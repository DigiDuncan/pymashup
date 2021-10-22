from pymashup.lib.getsongbpm import smart_search_songs


def main():
    song = smart_search_songs("megalovania")
    print([s for s in song if s.camelot is not None])


if __name__ == "__main__":
    main()
