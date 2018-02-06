# coding: utf-8
"""
/data/rawにカラム名のみの空のcsvテーブルを作成する
"""

import os

project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

columns = [
    'datetime',  # 画像保存時のdatetime ("%Y-%m-%d %H:%M:%S"形式)
    'title',  # 曲名
    'difficulty',  # 曲の難易度 (EASY, HARD, CHAOS)
    'level',  # 曲の難易度 (レベル)
    'score',  # スコア (~1000000)
    'is_best_score',  # スコア更新したかどうか
    'evaluation',  # 評価 (C, B, A, S)
    'tp',  # TP (単位: %)
    'max_combo',  # 最大コンボ数
    'perfect',  # PERFECT
    'good',  # GOOD
    'bad',  # BAD
    'miss',  # MISS
]


def main() -> None:
    # プレイログはdata/raw内に作成する
    data_raw_dir = os.path.join(project_dir, 'data', 'raw')

    # プレイログが未作成の場合のみ新規プレイログを作成する
    playlog_path = os.path.join(data_raw_dir, 'playlog.csv')
    if not os.path.exists(playlog_path):
        with open(playlog_path, 'w') as f:
            f.write(','.join(columns))
    else:
        raise FileExistsError("プレイログは作成済みなので何もしません")


if __name__ == '__main__':
    main()
