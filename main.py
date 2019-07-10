import sys
import requests
import spotipy
import spotipy.util as util

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

scope = 'playlist-modify-private'
token = util.prompt_for_user_token(username, scope)

if token:
    playlist_id = sys.argv[2]

    fip_url = 'https://www.fip.fr/latest/api/graphql';

    params = dict(
        operationName='Now',
        variables='{"bannerPreset":"600x600-noTransform","stationId":7,"previousTrackLimit":3}',
        extensions='{"persistedQuery":{"version":1,"sha256Hash":"8a931c7d177ff69709a79f4c213bd2403f0c11836c560bc22da55628d8100df8"}}',
    )
    resp = requests.get(url=fip_url, params=params)
    data = resp.json()

    try:
        song = data['data']['now']['song'];
    except KeyError:
        print(data)
        raise RuntimeError('No song found');

    if not song:
        raise RuntimeError('No song found');

    links = song['external_links'];

    if not links['spotify']:
        print(links)
        raise RuntimeError('No spotify song found');

    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist_add_tracks(username, playlist_id, ['spotify:track:' + links['spotify']['id']])
    print(results)
else:
    print("Can't get token for", username)
