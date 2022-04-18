
import pandas as pd

import meniscus
import proboscis

import sqlite3
from pathlib import Path
import os


def main():
    DATABASE = "feedings.db"

    QUERY = """SELECT *
    FROM videos
    INNER JOIN feedings
    ON videos.video_id = feedings.video_id;
    """

    con = sqlite3.connect(DATABASE)
    cursor = con.cursor()

    if not os.path.isdir("out"):
        os.mkdir("out")

    for i, row in enumerate(cursor.execute(QUERY)):
        filename = row[1]
        print(filename)
        path = Path(filename)
        stem = path.stem
        start_frame = row[4]
        end_frame = row[5]
        try:
            prob_xs, prob_ys = proboscis.get_proboscis(filename, start_frame, end_frame)
            men_xs, men_ys = meniscus.get_meniscus(filename, start_frame, end_frame)
        except:
            message = "{} failed within bounds {} to {}".format(filename,
                                                                start_frame,
                                                                end_frame)
            print(message)
            continue

        men_df = pd.DataFrame(zip(men_xs, men_ys),
                              columns=("frame_number","row_coordinate")
                              )
        prob_df = pd.DataFrame(zip(prob_xs, prob_ys),
                               columns=("frame number", "row_coordinate")
                               )
        fname_men = "out/{}-meniscus-{}.csv".format(stem, i)
        fname_pr = "out/{}-proboscis-{}.csv".format(stem, i)

        men_df.to_csv(fname_men)
        prob_df.to_csv(fname_pr)

    cursor.close()
    con.close()


if __name__ == '__main__':
    main()
