# coding: utf-8
"""
`load_result` により画像を読み込みセグメントごとにスライスする
"""

import os
import warnings
from datetime import datetime
from typing import List, Tuple, Dict, Generator
import numpy as np
import skimage.io

Segment = Dict[str, np.ndarray]

project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

filename_format = 'result_%Y%m%d_%H%M%S.jpg'
# datetime_format = '%Y-%m-%d %H:%M:%S'
division_rule = {
    'iPhone': {
        'title': (50, 150, 380, 1880),
        'difficulty_and_level': (152, 192, 900, 1300),
        'score': (600, 700, 80, 780),
        'is_best_score': (545, 595, 280, 600),
        'evaluation': (420, 600, 1000, 1200),
        'tp': (725, 775, 960, 1240),
        'max_combo': (600, 700, 1550, 1950),
        'perfect': (1120, 1180, 640, 840),
        'good': (1120, 1180, 865, 1065),
        'bad': (1120, 1180, 1090, 1290),
        'miss': (1120, 1180, 1315, 1515),
    },
    'iPad': {
        'title': (50, 150, 380, 1880),
        'difficulty_and_level': (141, 179, 850, 1250),
        'score': (750, 850, 100, 750),
        'is_best_score': (695, 745, 270, 560),
        'evaluation': (580, 750, 950, 1100),
        'tp': (865, 915, 900, 1150),
        'max_combo': (750, 850, 1450, 1850),
        'perfect': (1420, 1480, 590, 790),
        'good': (1420, 1480, 795, 995),
        'bad': (1420, 1480, 1000, 1200),
        'miss': (1420, 1480, 1205, 1405),
    },
}


def _parse_datetime_by_path(path: str) -> datetime:
    """画像パスからdatetimeを取得する"""
    assert isinstance(path, str)
    filename = os.path.basename(path)
    try:
        dt = datetime.strptime(filename, filename_format)
    except ValueError as e:
        raise e
    return dt


def _get_paths_in_raw() -> List[str]:
    """data/rawディレクトリのパス一覧を取得する"""
    raw_dir = os.path.join(project_dir, 'data', 'raw')
    return os.listdir(raw_dir)


def _slice_image_by_division_rule(
        image: np.ndarray, device: str, segmentation_name: str) -> np.ndarray:
    """division_ruleに従ってスクリーンショットを分割する"""
    try:
        i0, i1, j0, j1 = division_rule[device][segmentation_name]
    except IndexError as e:
        warnings.warn(
            'スクリーンショットの分割に失敗しました。'
            'おそらくdivision_ruleが不適切なので、再度確認してください。'
        )
        raise e
    return image[i0:i1, j0:j1]


def _open_image(path: str) -> np.ndarray:
    """floatのグレースケールで画像を開く"""
    assert isinstance(path, str)
    assert os.path.exists(path)

    try:
        image = skimage.io.imread(path, as_grey=True)
    except OSError as e:
        warnings.warn(f'skimage.io.imreadは{path}を開けません。')
        raise e

    assert image.max() <= 1
    assert image.min() >= 0

    return image


def _get_device_name_by_size(size: Tuple[int, int]) -> str:
    """画像サイズからデバイス名を取得する"""
    assert isinstance(size, tuple)

    if size == (1242, 2208):
        return 'iPhone'
    elif size == (1536, 2048):
        return 'iPad'
    else:
        raise ValueError(
            f'{size} は不適切なsizeです。iPhoneならsizeは (2208, 1242) に、'
            'iPadならsizeは (2048, 1536) になるはずです'
        )
    return size


def generate_result_information() -> Generator[datetime, str, Segment]:
    paths = _get_paths_in_raw()
    raise Exception()
    for path in paths:
        # リザルト画像以外へのファイルパスが渡された場合は無視する
        try:
            dt = _parse_datetime_by_path(path)
        except ValueError:
            continue

        # リザルト画像が壊れていて開けなかった場合は無視する
        try:
            image = _open_image(path)
        except OSError:
            continue

        device = _get_device_name_by_size(image.shape)

        segment = {'entire': image}
        for key in division_rule[device].keys():
            segment[key] = _slice_image_by_division_rule(image, device, key)

        yield dt, device, segment
