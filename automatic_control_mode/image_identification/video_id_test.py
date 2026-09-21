import threading
import time
from detect import detect
import numpy as np
import cv2 as cv2
from communication import Communication as com
from communication import find_camera
from move import operation
from multiprocessing import Process
import os, time
import csv
from datetime import datetime
import math

# import Matplotlab as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


videoname = '4_19_human_demoorigin'
# videoname = '60_ms'

# frames_to_skip = 370
frames_to_skip = 50

frames_to_end = frames_to_skip + 300

k_px2w_6dot7 = 0.0577
# path = os.path.join(BASE_DIR, "test_video_group", videoname + "orign.mp4")
path = os.path.join(BASE_DIR, "test_video_group", videoname + ".mp4")
# path="D:/throat swab/video/test_video/"+videoname+"orign.mp4"
cap, retu = find_camera().open_camera(cam_n=None, path=path)
print("Is video open successfull:", retu)
print("Video route:", path)


cx = 640
de = detect(thresh_draw=True, contour_draw=True, circle_draw=True, n_cl=3)
ready_to_sampling = True

x1 = 500   # Valid region: top-left x
y1 = 250  # Valid region: bottom-right y
x2 = 740# Valid region: bottom-right x
y2 = 50   # Valid region: top-left y
x_0 = 510
y_0 = 665

# if (cx < x2 and cx > x1 and cy < y1 and cy > y2):

# ============ Mouse callback state (module-level globals) ============
drawing = False
ix, iy = -1, -1
ex, ey = -1, -1
rect_done = False

# Calibration parameters kept consistent with pixel_to_angle in communication.py
PIXEL_CENTER_CAL = (640, 150)  # Image center pixel
PIXEL_RATIO = 0.05             # mm/pixel

# Z0 = 190.5
Z0 = 175

target_angle = 2

k_px2w = k_px2w_6dot7
file_path = "D:/ajc/Pharyngeal_swab_robot/video_cbl/"
gt_results_dir = os.path.join(BASE_DIR, "Ground_Truth_choose_Frames_cbl")
results_dir = os.path.join(BASE_DIR, "results_cbl")
target_length = 6 / k_px2w
file1 = videoname + '_test1.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4
fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter(file_path + file1, fourcc, 25, size)


def mouse_callback(event, x, y, flags, param):
    """Mouse callback for drawing a single rectangle by click-and-drag."""
    global ix, iy, ex, ey, drawing, rect_done
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        ex, ey = x, y
        rect_done = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            ex, ey = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        ex, ey = x, y
        rect_done = True


def reset_rect():
    """Reset the rectangle state so the user can draw a new one."""
    global ix, iy, ex, ey, drawing, rect_done
    ix, iy, ex, ey = -1, -1, -1, -1
    drawing = False
    rect_done = False


def annotate_gt(frame_clean, frame_number, algo_cx, algo_cy):
    """
    Open an annotation window on the given frame.
    The user draws THREE rectangles in sequence; after each rectangle
    press SPACE to confirm, R to redraw, Q to abort.
    The averaged center of the three rectangles is returned as the
    ground-truth coordinate in the pixel coordinate system.
    """
    window_name = "GT Annotation - Draw 3 rectangles | SPACE=confirm | R=redraw | Q=abort"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name, mouse_callback)

    centers = []  # List of confirmed rectangle centers: [(cx1, cy1), ...]

    print("\n" + "=" * 60)
    print(f"GT annotation started on frame {frame_number}")
    print(f"Algorithm-detected center: ({algo_cx}, {algo_cy})")
    print("Please draw 3 rectangles around the target region.")
    print("=" * 60)

    round_idx = 0
    while round_idx < 3:
        reset_rect()
        print(f"\n--> Rectangle {round_idx + 1}/3 : drag with the left mouse button")

        while True:
            display = frame_clean.copy()

            # Draw previously confirmed rectangle centers in blue for reference
            for k, (pcx, pcy) in enumerate(centers):
                cv2.circle(display, (pcx, pcy), 6, (255, 100, 0), -1)
                cv2.putText(display, f"#{k + 1}", (pcx + 8, pcy - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 0), 2)

            # Top info bar
            info = (f"Frame {frame_number}  |  Rect {round_idx + 1}/3  |  "
                    f"SPACE=confirm  R=redraw  Q=abort")
            cv2.putText(display, info, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            # Draw the rectangle currently being edited in green
            if ix != -1 and (drawing or rect_done):
                cv2.rectangle(display, (ix, iy), (ex, ey), (0, 255, 0), 2)
                if rect_done:
                    cur_cx = (ix + ex) // 2
                    cur_cy = (iy + ey) // 2
                    cv2.circle(display, (cur_cx, cur_cy), 5, (0, 0, 255), -1)
                    cv2.putText(display, f"({cur_cx},{cur_cy})",
                                (cur_cx + 10, cur_cy - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            cv2.imshow(window_name, display)
            key = cv2.waitKey(20) & 0xFF

            if key == ord('q'):
                cv2.destroyWindow(window_name)
                print("Annotation aborted by user.")
                return None, None, None
            elif key == ord('r'):
                reset_rect()
                print("  Rectangle cleared, please redraw.")
            elif key == ord('S'):  # Shift+s: skip this attempt, wait for the next 10-frame streak
                cv2.destroyWindow(window_name)
                print("GT attempt skipped. Waiting for the next 10-frame streak.")
                return "skip", None, None
            elif key == ord(' '):  # SPACE confirms the current rectangle
                if not rect_done:
                    print("  No rectangle drawn yet. Please drag the mouse first.")
                    continue

                cur_cx = (ix + ex) // 2
                cur_cy = (iy + ey) // 2
                centers.append((cur_cx, cur_cy))
                print(f"  Rect {round_idx + 1} confirmed, center = ({cur_cx}, {cur_cy})")
                break
        round_idx += 1

    cv2.destroyWindow(window_name)

    # Compute ground-truth center as the average of the 3 rectangle centers
    xs = np.array([c[0] for c in centers])
    ys = np.array([c[1] for c in centers])
    gt_cx = int(round(xs.mean()))
    gt_cy = int(round(ys.mean()))

    return centers, gt_cx, gt_cy


def draw_gt_marker(image, gt_cx, gt_cy):
    """Overlay the ground-truth point on the given image."""

    color = (0, 255, 255)   # Yellow in BGR
    # Outer ring
    cv2.circle(image, (gt_cx, gt_cy), 14, color, 2)
    # Small filled center dot
    cv2.circle(image, (gt_cx, gt_cy), 3, color, -1)
    # Crosshair lines
    cv2.line(image, (gt_cx - 25, gt_cy), (gt_cx - 8, gt_cy), color, 2)
    cv2.line(image, (gt_cx + 8, gt_cy), (gt_cx + 25, gt_cy), color, 2)
    cv2.line(image, (gt_cx, gt_cy - 25), (gt_cx, gt_cy - 8), color, 2)
    cv2.line(image, (gt_cx, gt_cy + 8), (gt_cx, gt_cy + 25), color, 2)
    # Text label
    cv2.putText(image, f"GT ({gt_cx},{gt_cy})",
                (gt_cx + 18, gt_cy - 18),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return image



def pixel_to_angle_deg(px, py):
    """Pixel -> motor angle (degrees). Excludes the motor zero-position offset and the *10 scaling; returns the geometric angle only."""
    ang_x = math.degrees(math.atan((px - PIXEL_CENTER_CAL[0]) * PIXEL_RATIO / Z0))
    ang_y = math.degrees(math.atan((py - PIXEL_CENTER_CAL[1]) * PIXEL_RATIO / Z0))
    # ang_x = math.degrees(math.atan((px) * PIXEL_RATIO / Z0))
    # ang_y = math.degrees(math.atan((py) * PIXEL_RATIO / Z0))
    return ang_x, ang_y

def angle_deg_to_pixel(ang_x, ang_y):
    rad_x = math.radians(ang_x)
    rad_y = math.radians(ang_y)
    px = math.tan(rad_x) * Z0 / PIXEL_RATIO + PIXEL_CENTER_CAL[0]
    py = math.tan(rad_y) * Z0 / PIXEL_RATIO + PIXEL_CENTER_CAL[1]
    # px = math.tan(rad_x) * Z0 / PIXEL_RATIO
    # py = math.tan(rad_y) * Z0 / PIXEL_RATIO
    return px, py

def main_fun(de):



    in_position = [640, 150]
    i = 0
    success_count = 0       # Successful detections
    fail_count = 0          # Failed detections
    gt_captured = False     # Whether GT annotation has already been performed
    gt_captured_saveFrames = False
    test_num = 0            # Consecutive-in-region frame counter



    px_t1 = 0
    py_t1 = 0
    px_t2 = 0
    py_t2 = 0

    box_initialized = False

    # Persistent GT coordinates: initialized to None; filled in once annotation is done
    gt_cx = None
    gt_cy = None

    gt_ang_x = None
    gt_ang_y = None

    while 1:
        ret, image = cap.read()
        if ret == True:
            i += 1
            # print('item = ', i)
            if i % 1 == 0:
                # Keep a clean copy of the raw frame BEFORE detection markers are drawn
                if i > frames_to_end :
                    break
                image_clean = image.copy()


                cx = cy = None   # Reset per-frame detection result
                if  i < frames_to_skip :
                    continue
                else:
                    try:
                        start = time.time()
                        image, cx, cy = de.find_xy(image)
                        success_count += 1
                        end = time.time()


                        algo_ang_x, algo_ang_y = pixel_to_angle_deg(cx, cy)

                        if not box_initialized:
                            px_t1 = cx - target_length/2
                            py_t1 = cy - target_length/2
                            px_t2 = cx + target_length/2
                            py_t2 = cy + target_length/2
                            box_initialized = True

                        if (cx <= px_t2 and cx >= px_t1 and cy <= py_t2 and cy >= py_t1):

                        # if (cx < x2 and cx > x1 and cy < y1 and cy > y2):
                            test_num = test_num + 1
                            # print("test num is://", test_num)
                            if test_num >= 10 and not gt_captured:
                                ready_to_sampling = True
                                in_position = [cx, cy]
                                print("center in position is://", in_position, "//")
                                centers, gt_cx, gt_cy = annotate_gt(image_clean, i, cx, cy)


                                # Guard against the user aborting the annotation (Q key)
                                if centers == "skip":
                                    test_num = 0  # Reset counter, wait for a new 10-frame streak
                                    # gt_captured stays False so the next streak can re-trigger annotation
                                    print(f"Skipped at frame {i}. Counter reset to 0.")


                                elif gt_cx is None:
                                    # User pressed Q — abort permanently, never try again
                                    print("GT annotation was aborted. Will not overlay GT.")
                                    gt_captured = True
                                else:
                                    gt_captured = True
                                    gt_captured_saveFrames = True
                                    gt_ang_x, gt_ang_y = pixel_to_angle_deg(gt_cx, gt_cy)
                                    algo_ang_x, algo_ang_y = pixel_to_angle_deg(cx, cy)

                                    # px_c_1 = int(round(angle_deg_to_pixel(gt_ang_x - 1, gt_ang_y - 1)[0]))
                                    # py_c_1 = int(round(angle_deg_to_pixel(gt_ang_x - 1, gt_ang_y - 1)[1]))
                                    # px_c_2 = int(round(angle_deg_to_pixel(gt_ang_x + 1, gt_ang_y + 1)[0]))
                                    # py_c_2 = int(round(angle_deg_to_pixel(gt_ang_x + 1, gt_ang_y + 1)[1]))

                                    xs = np.array([c[0] for c in centers])
                                    ys = np.array([c[1] for c in centers])
                                    std_x = float(xs.std())
                                    std_y = float(ys.std())
                                    mean_dist = float(np.sqrt(((xs - gt_cx) ** 2 + (ys - gt_cy) ** 2)).mean())
                                    algo_error = float(np.sqrt((cx - gt_cx) ** 2 + (cy - gt_cy) ** 2))
                                    algo_ang_error = float(np.sqrt((algo_ang_x - gt_ang_x) ** 2 +
                                                                   (algo_ang_y - gt_ang_y) ** 2))
                                    w_cor_x = (cx - gt_cx) * k_px2w
                                    w_cor_y = (cy - gt_cy) * k_px2w
                                    w_cor_error = float(np.sqrt(w_cor_x ** 2 + w_cor_y ** 2))
                                    rmse_w_cor = np.sqrt(np.mean((w_cor_x ** 2 + w_cor_y ** 2)))

                                    print("\n" + "=" * 60)
                                    print("GT annotation finished")
                                    print(f"  GT (pixel coords)   : ({gt_cx}, {gt_cy})")
                                    print(f"  Algorithm error     : {algo_error:.2f} px")
                                    print("=" * 60 + "\n")
                                    print(f"  GT  angle (deg)     : ({gt_ang_x:.3f}, {gt_ang_y:.3f})")
                                    print(f"  Algo angle (deg)    : ({algo_ang_x:.3f}, {algo_ang_y:.3f})")
                                    print(f"  Algo angle error    : {algo_ang_error:.3f} deg")

                                    # Append the result to a CSV file
                                    # csv_path = os.path.join(results_dir, videoname + "gt_annotations.csv")
                                    csv_path = os.path.join(results_dir,   "All_video_gt_annotations.csv")
                                    csv_exists = os.path.exists(csv_path)
                                    with open(csv_path, "a", newline="", encoding="utf-8") as f:
                                        writer = csv.writer(f)
                                        if not csv_exists:
                                            writer.writerow([
                                                "video", "frame_number",
                                                "rect1_cx", "rect1_cy",
                                                "rect2_cx", "rect2_cy",
                                                "rect3_cx", "rect3_cy",
                                                "gt_cx", "gt_cy",
                                                "std_x_px", "std_y_px", "mean_dist_px",
                                                "algo_cx", "algo_cy", "algo_error_px",
                                                'algo_ang_error', 'w_cor_x', 'w_cor_y',
                                                'w_cor_err', 'rmse_w_cor'
                                            ])
                                        writer.writerow([
                                            videoname, i,
                                            centers[0][0], centers[0][1],
                                            centers[1][0], centers[1][1],
                                            centers[2][0], centers[2][1],
                                            gt_cx, gt_cy,
                                            f"{std_x:.2f}", f"{std_y:.2f}", f"{mean_dist:.2f}",
                                            cx, cy, f"{algo_error:.2f}", f"{algo_ang_error:.2f}",
                                            f"{w_cor_x:.2f}",  f"{w_cor_y:.2f}",  f"{w_cor_error:.2f}",
                                            f"{rmse_w_cor:.2f}",
                                        ])
                                    print(f"Result appended to: {csv_path}")
                        elif not gt_captured:
                            px_t1 = cx - target_length / 2
                            py_t1 = cy - target_length / 2
                            px_t2 = cx + target_length / 2
                            py_t2 = cy + target_length / 2
                            test_num = 0
                        else:
                            test_num = 0

                    except Exception as e:
                        fail_count += 1
                        test_num = 0
                        # print(f'The {i} th image detected failed!', e)
                        # print('NO detected!', e)

                # ---------- Overlay the GT marker on every frame after capture ----------
                # Once GT has been captured, every subsequent frame (successful or failed
                # detection) shows the yellow GT crosshair at the fixed pixel location.
                    if gt_captured  and gt_cx is not None:
                        draw_gt_marker(image, gt_cx, gt_cy)

                        # Also print per-frame error vs GT if the detection succeeded this frame
                        if cx is not None and cy is not None:
                            err_px = float(np.sqrt((cx - gt_cx) ** 2 + (cy - gt_cy) ** 2))
                            cv2.putText(image, f"err={err_px:.1f}px",
                                        (gt_cx + 18, gt_cy + 6),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
                            ang_x, ang_y = pixel_to_angle_deg(cx, cy)
                            err_deg = float(np.sqrt((ang_x - gt_ang_x) ** 2 +
                                                    (ang_y - gt_ang_y) ** 2))

                            wcor_x = (cx - gt_cx) * k_px2w
                            wcor_y = (cy - gt_cy) * k_px2w
                            wcor_error = float(np.sqrt(wcor_x ** 2 + wcor_y ** 2))
                            rmse_w_cor1 = np.sqrt(np.mean((wcor_x ** 2 + wcor_y ** 2)))
                            cv2.putText(image, f"w_err={wcor_error:.2f}mm",
                                        (gt_cx + 18, gt_cy + 26),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
                            cv2.putText(image, f"w_x={wcor_x:.2f}mm",
                                        (gt_cx + 18, gt_cy + 45),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
                            cv2.putText(image, f"w_y={wcor_y:.2f}mm",
                                        (gt_cx + 18, gt_cy + 64),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)


                    # if cx is not None and cy is not None:
                    #     cv2.rectangle(image, (px_c_1, py_c_1), (px_c_2, py_c_2), (0, 255, 255), 2)
                    if box_initialized :
                        px_t1 = int(px_t1)
                        py_t1 = int(py_t1)
                        px_t2 = int(px_t2)
                        py_t2 = int(py_t2)
                        # l_px = (x2 - x1) * k_px2w
                        # l_py = (y1 - y2) * k_px2w
                        l_px = (px_t2 - px_t1) * k_px2w
                        l_py = (py_t2 - py_t1) * k_px2w
                        # print('l_x:', l_px, 'l_y:', l_py)
                        # print('px_t1:', px_t1, 'py_t1:', py_t1, 'px_t2:', px_t2, 'py_t2:', py_t2)
                        cv2.rectangle(image, (px_t1, py_t1), (px_t2, py_t2), (0, 255, 255), 2)

                    if gt_captured_saveFrames :
                        filename = f"{videoname}_GT_choose_frame.jpg"
                        filepath = os.path.join(gt_results_dir, filename)
                        ok = cv2.imwrite(filepath, image)
                        if ok:
                            print(f"[Saved] frame  -> {filepath}")
                        else:
                            print(f"[ERROR] failed to save frame to {filepath}")
                        gt_captured_saveFrames = False


                    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                    cv2.imshow('image', image)
                    cv2.waitKey(1)
                    out.write(image)
                    # cv2.imwrite(path+'picture/'+str(i)+'.jpg', image)

        else:
            print('item:', i)
            print(f"Total successful detections: {success_count}")
            print(f"Total failed detections:     {fail_count}")
            if gt_cx is not None:
                print(f"Ground-truth coordinate (pixel): ({gt_cx}, {gt_cy})")
            break
    return in_position


if __name__ == "__main__":
    center = main_fun(de)
    cap.release()
    out.release()
    # np.savetxt("force_list_"+videoname+"or.txt", force_list)
    # cv2.destroyAllWindows()
    # open_app(r'C:\Users\22135\Desktop\xxx')
    # sampling(opera, True, center)