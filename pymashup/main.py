from pymashup.lib.getsongbpm import search_song


def main():
    song = search_song("blinding lights")
    print(song)


if __name__ == "__main__":
    main()
