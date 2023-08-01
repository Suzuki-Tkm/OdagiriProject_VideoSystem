import cv2
import os
import time

# 動画の読み込み
# cap = cv2.VideoCapture("/Users/apple/project/frame.mp4")
video = cv2.VideoCapture("/Users/apple/project/frame.mp4")
# 画像フォルダーのパス
image_folder_path = "/Users/apple/project/picture"

# 動画フォルダーのパス
video_folder_path = "/Users/apple/project/video"

# 最初に画像が読み込まれていないため、最初の画像のファイル名を格納するための変数を定義
previous_image = None
previous_video = None

# 最後に画像が読み込まれた時刻を格納する変数
last_image_load_time = time.time()
last_video_load_time = time.time()

# メインループ
while True:
    videos = os.listdir(video_folder_path)
    videos.sort(reverse=True)
    latest_video = None

    for video in videos:
        if video.endswith(".mp4"):
            latest_video = os.path.join(video_folder_path, video)
            break
    
    if latest_video != previous_video:
        
        video = cv2.VideoCapture(latest_video)
        last_video_load_time = time.time()

    # 動画から1フレームを読み込む
    ret, frame = video.read()
    
    # 動画が終わったらループを抜ける
    if not ret:
        break
    
    # 画像フォルダー内の最新の画像を取得
    images = os.listdir(image_folder_path)
    images.sort(reverse=True)
    latest_image = None
    
    # 最新の画像を探す
    for image in images:
        if image.endswith(".JPG") or image.endswith(".png"):
            latest_image = os.path.join(image_folder_path, image)
            break
    
    # 前回の画像と異なる場合、新しい画像を読み込む
    if latest_image != previous_image:
        # 画像の読み込み
        image = cv2.imread(latest_image)

        # 画像のリサイズ
        image = cv2.resize(image, (512, 512))

        # 画像を表示する位置を計算する
        x_offset = int((frame.shape[1] - image.shape[1]) / 2)
        y_offset = int((frame.shape[0] - image.shape[0]) / 2)

        # 背景画像に画像を追加する
        frame[y_offset:y_offset+image.shape[0], x_offset:x_offset+image.shape[1]] = image

        # 最後に画像が読み込まれた時刻を更新する
        last_image_load_time = time.time()

    # 動画を再生する
    cv2.imshow("frame", frame)

    # キー入力を待つ
    key = cv2.waitKey(1)

    # 'q'が入力された場合、ループを抜ける
    if key == ord("q"):
        break
    
    # 5秒以上経過していたら、新しい画像が追加されていないか確認する
    if time.time() - last_image_load_time > 5:
        continue

video.release()
cv2.destroyAllWindows()
