import argparse
import stream
import mongo


def main():
    args = parse_args()
    db = mongo.get_mongo_database_with_auth(args.dbhost, args.dbport, args.dbname, args.username, args.password)

    year = int(args.phrase_year)
    query = db[args.phrase_collection].find({'year': year})
    titles = []
    for cursor in query:
        titles.append(cursor['title'][:-7])
    stream.init_crawler(args.consumer_key, args.consumer_secret, args.access_token, args.access_token_secret,
                        db[args.collection], titles)

def parse_args():
    parser = argparse.ArgumentParser()

    # Mongo params
    parser.add_argument('--dbhost', help='Address of MongoDB server', default="127.0.0.1")
    parser.add_argument('--dbport', help='Port of MongoDB server', default=27017)
    parser.add_argument('--dbname', '-n', help='Database name', type=str, required=True)
    parser.add_argument('--username', help='Database user', default=None)
    parser.add_argument('--password', help='Password for the user', default=None)
    parser.add_argument('--collection', '-v', help='Collection name for Twitter stream data',
                        default="twitter_stream")

    # Twitter params
    parser.add_argument('--consumer_key', help='Twitter api consumer key', required=True)
    parser.add_argument('--consumer_secret', help='Twitter api consumer secret', required=True)
    parser.add_argument('--access_token', help='Twitter api access token', required=True)
    parser.add_argument('--access_token_secret', help='Twitter api access token secret', required=True)
    parser.add_argument('--phrase_collection', help='Phrase collection', required=True)
    parser.add_argument('--phrase_year', help='Twitter search phrases comma seperated', required=True)

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nGoodbye!'
