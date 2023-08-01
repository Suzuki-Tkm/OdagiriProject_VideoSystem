import os
import time
from obswebsocket import obsws, requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# OBSの接続設定
ws = obsws("localhost", 4444)  # OBSのホストとポート番号に合わせて変更
ws.connect()

# 画像フォルダのパス
image_folder = "./picture"  # 表示したい画像が保存されているフォルダのパスに変更

# OBSのシーン名
scene_name = "Scene Name"  # 画像を表示させるOBSのシーン名に変更

# 最新画像の表示関数
def display_latest_image():
    image_files = sorted(os.listdir(image_folder), key=os.path.getmtime, reverse=True)
    if len(image_files) > 0:
        latest_image = image_files[0]
        ws.call(requests.SetSceneItemProperties(scene_name, visible=False))
        ws.call(requests.SetImageRender(latest_image, True))
        ws.call(requests.SetSceneItemProperties(scene_name, visible=True))

# フォルダの変更監視クラス
class ImageFolderEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.event_type == 'created' or event.event_type == 'modified':
            display_latest_image()

# フォルダの変更監視の開始
event_handler = ImageFolderEventHandler()
observer = Observer()
observer.schedule(event_handler, path=image_folder, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()

ws.disconnect()