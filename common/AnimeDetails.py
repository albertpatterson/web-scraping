class AnimeDetails:

    header = "\t".join([
        'name',
        'mediaType',
        'episodes',
        'startDate',
        'studios',
        'genres',
        'rating',
        'score',
        'members',
        'url',
    ])

    def __init__(
        self,
        name,
        mediaType,
        episodes,
        startDate,
        studios,
        genres,
        rating,
        score,
        members,
        url,
    ):
        self.name = name
        self.mediaType = mediaType
        self.episodes = episodes
        self.startDate = startDate
        self.studios = studios
        self.genres = genres
        self.rating = rating
        self.score = score
        self.members = members
        self.url = url

    def __str__(self):
        return '\t'.join([
            self.name,
            self.mediaType,
            self.episodes,
            self.startDate,
            self.studios,
            self.genres,
            self.rating,
            self.score,
            self.members,
            self.url,
        ])
