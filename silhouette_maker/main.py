# サードパーティライブラリ
import webuiapi
from PIL import Image, ImageChops

# WebUIのデフォルトでのローカルホスト、ポート番号
IMAGE_SERVER_HOST = "127.0.0.1"
IMAGE_SERVER_PORT = "7860"

# プロンプト
PROMPT = """white background, photo of {prompt}, SIGMA 50mm F1.4, artstation, deviantart,"""\
    """very cute, big eyes, extremely detailed eyes and face, eyes with beautiful details, looking at viewer"""
NEGATIVE_PROMPT = """(worst quality:2) (low quality:2) (normal quality:2) """\
    """lowers normal quality ((monochrome)) ((grayscale)),skin spots,acnes,skin blemishes,age spot,ugly face"""\
    """illust,character,ukiyo-e,painting,digital painting,doll,nsfw,text"""

# ControlNetに入力する画像
MEDIA_PIPE_FACE_IMAGE = "./img/bace_face.png"

# 生成画像時の設定
IMAGE_WIDTH = 568
IMAGE_HEIGHT = 768
BATCH_SIZE = 1


def _make_silhouette(image_seg: Image.Image, image_depth: Image.Image) -> Image.Image:
    # 人物切り抜き用のマスクの作成
    base_image = image_seg.copy()
    src_color = (150, 5, 61)    # 人物の色がセグメンテーションされる色
    _r, _g, _b = base_image.split()
    _r = _r.point(lambda x: 1 if src_color[0] - 5 < x < src_color[0] + 5 else 0, mode="1")
    _g = _g.point(lambda x: 1 if src_color[1] - 5 < x < src_color[1] + 5 else 0, mode="1")
    _b = _b.point(lambda x: 1 if src_color[2] - 5 < x < src_color[2] + 5 else 0, mode="1")
    mask = ImageChops.logical_and(_r, _g)
    mask = ImageChops.logical_and(mask, _b)
    base_image.putalpha(mask)

    # 深度画像を反転させて透明度を付与
    inverted_depth = Image.eval(image_depth, lambda x: 255 - x)
    base_image.paste((0, 0, 0, 0), (0, 0), inverted_depth)
    return base_image


def _generate_image(image_api: webuiapi.WebUIApi, prompt: str = "man, ") -> list[Image.Image]:
    # 人物の画像生成を行う

    # ControlNetの設定
    model_name = None
    for controlnet_model in image_api.controlnet_model_list():
        if "mediapipe_face" in controlnet_model:
            model_name = controlnet_model
    base_face_img = Image.open(MEDIA_PIPE_FACE_IMAGE)
    unit_base_face = webuiapi.ControlNetUnit(
        input_image=base_face_img,
        module='none',
        model=model_name
    )
    control_net_unit = [unit_base_face]

    prompt = PROMPT.format(prompt=prompt)
    result = image_api.txt2img(
        prompt=prompt,
        negative_prompt=NEGATIVE_PROMPT,
        width=IMAGE_WIDTH,
        height=IMAGE_HEIGHT,
        batch_size=BATCH_SIZE,
        controlnet_units=control_net_unit
    )
    return result.images


def _get_masks(image_api: webuiapi.WebUIApi, image: Image.Image) -> tuple[Image.Image, Image.Image]:
    # マスク画像を作成する
    width = image.width
    image_seg = image_api.controlnet_detect([image], module="oneformer_ade20k", processor_res=width).image
    image_depth = image_api.controlnet_detect([image], module="depth_zoe", processor_res=width).image
    return image_seg, image_depth


def _main() -> None:
    # WebUIに接続
    image_api = webuiapi.WebUIApi(IMAGE_SERVER_HOST, IMAGE_SERVER_PORT)

    # 元画像を生成
    images = _generate_image(image_api)

    for i, image in enumerate(images):
        if i != len(images) - 1:
            # 生成された元画像を保存
            image.save(f"./base_image{i}.png")

            # 影絵を作成
            image_seg, image_depth = _get_masks(image_api, image)
            img = _make_silhouette(image_seg, image_depth)

            # 影絵を保存
            img.save(f"./silhouette_image{i}.png")


if __name__ == "__main__":
    _main()
