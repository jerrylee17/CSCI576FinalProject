from util.io import read_video, display_video

def test_video():
    video = read_video("../videos/SAL_490_270_437")
    display_video(video)



if __name__ == '__main__':
    test_video()
