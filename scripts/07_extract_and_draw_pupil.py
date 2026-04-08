import os
import cv2
import argparse
import numpy as np


def find_first_video(root: str):
    exts = (".avi", ".mp4", ".mov", ".mkv")
    candidates = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.lower().endswith(exts):
                candidates.append(os.path.join(dirpath, fn))
    candidates.sort()
    return candidates[0] if candidates else None


def detect_pupil(frame_gray: np.ndarray):
    h, w = frame_gray.shape

    blur = cv2.GaussianBlur(frame_gray, (7, 7), 0)

    # dark pupil: inverse threshold + Otsu
    _, th = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    kernel = np.ones((3, 3), np.uint8)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=1)
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    best = None
    best_score = -1e18
    img_area = h * w

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 150 or area > img_area * 0.25:
            continue
        if len(cnt) < 5:
            continue

        x, y, cw, ch = cv2.boundingRect(cnt)
        aspect = cw / max(ch, 1)
        if aspect < 0.3 or aspect > 3.0:
            continue

        cx = x + cw / 2.0
        cy = y + ch / 2.0
        center_dist = ((cx - w / 2) ** 2 + (cy - h / 2) ** 2) ** 0.5

        # prefer reasonably large, central candidates
        score = area - 0.2 * center_dist

        if score > best_score:
            best_score = score
            best = cnt

    if best is None:
        return None, th

    ellipse = cv2.fitEllipse(best)
    (cx, cy), (ma, mi), angle = ellipse

    return {
        "contour": best,
        "center": (int(cx), int(cy)),
        "ellipse": ellipse,
        "major_minor": (float(ma), float(mi)),
        "angle": float(angle),
    }, th


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str, default=None, help="explicit video path")
    parser.add_argument("--root", type=str, default="data/raw_eye_videos/LPW", help="search root if --video is not given")
    parser.add_argument("--frame-step", type=int, default=30, help="save every Nth frame")
    parser.add_argument("--max-frames", type=int, default=20, help="maximum number of frames to export")
    args = parser.parse_args()

    video_path = args.video if args.video else find_first_video(args.root)
    if video_path is None:
        raise FileNotFoundError(
            f"No video found under: {args.root}. "
            "Try: find data/raw_eye_videos/LPW -type f | head"
        )

    print(f"Using video: {video_path}")

    os.makedirs("outputs/eye_frames", exist_ok=True)
    os.makedirs("outputs/pupil_overlays", exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    frame_id = 0
    saved = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        if frame_id % args.frame_step != 0:
            frame_id += 1
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result, mask = detect_pupil(gray)

        raw_path = f"outputs/eye_frames/frame_{frame_id:06d}.png"
        overlay_path = f"outputs/pupil_overlays/frame_{frame_id:06d}_overlay.png"
        mask_path = f"outputs/pupil_overlays/frame_{frame_id:06d}_mask.png"

        cv2.imwrite(raw_path, gray)

        vis = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        if result is not None:
            cv2.drawContours(vis, [result["contour"]], -1, (0, 255, 0), 2)
            cv2.ellipse(vis, result["ellipse"], (0, 0, 255), 2)
            cv2.circle(vis, result["center"], 3, (255, 0, 0), -1)

        cv2.imwrite(overlay_path, vis)
        cv2.imwrite(mask_path, mask)

        print(f"saved frame {frame_id}: {raw_path}, {overlay_path}, {mask_path}")

        saved += 1
        frame_id += 1

        if saved >= args.max_frames:
            break

    cap.release()
    print(f"Done. Saved {saved} frames.")


if __name__ == "__main__":
    main()
