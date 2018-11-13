import argparse
import re
import json
import matplotlib.pyplot as plt
import numpy as np

keys = {}
metrics = {}
token_families = {}


def plot_histogram(data, normalize, title):
    labels = []
    values = []

    for key, val in data.items():
        labels.append(key)
        values.append(val)

    # sort on labels
    values = [v for _,v in sorted(zip(labels, values))]
    labels = sorted(labels)

    values = np.array(values).astype(float)
    if normalize:
        values /= np.sum(values)


    plt.title(title)
    plt.bar(np.arange(len(labels)), values)
    plt.xticks(np.arange(len(labels)), labels, rotation=70)
    plt.show()

def analyze(filename):

    # Taken from the parser
    re_key = re.compile(r"\\?\[?K:\s?[ABCDEFG][#b]?\s?(major|maj|m|minor|min|mixolydian|mix|dorian|dor|phrygian|phr|lydian|lyd|locrian|loc)?\]?", re.IGNORECASE)
    re_tempo = re.compile(r"\[?L\:\s?\d+\/\d+\s?\]?", re.IGNORECASE)
    re_meter = re.compile(r"\[?M\:\s?\d+\/\d+\s?\]?", re.IGNORECASE)
    re_duplets = re.compile(r"\([2-9]:?[2-9]?:?[2-9]?")
    re_note = re.compile(r"\^{0,2}\_{0,2}=?[A-Ga-g]'?,?")
    re_length = re.compile(r"[1-9]{0,2}\/{0,2}[1-9]{1,2}")
    re_length_short_2 = re.compile(r"/")
    re_length_short_4 = re.compile(r"//")
    re_rest = re.compile(r"z")
    re_repeat = re.compile(r":?\|\s?\[?\d")
    re_bar = re.compile(r":?\|:?")
    re_durations = re.compile(r"[<>]{1,2}")
    re_grouping = re.compile(r"[\[\]]")
    #Regex should be added in prority order since if one matches
    #it will stop
    regex_dict = {
            'key': re_key,
            'tempo': re_tempo,
            'meter': re_meter,
            'length': re_length,
            'duplets': re_duplets,
            'note': re_note,
            'repeat': re_repeat,
            'rest': re_rest,
            'bar': re_bar,
            'duration': re_durations,
            'grouping': re_grouping,
            'length_2': re_length_short_2,
            'length_4': re_length_short_4
            }

    with open(filename, 'r') as f:
        for line in f:
            tokens = line.split()
            for token in tokens:
                for token_family, reg in regex_dict.items():
                    match = reg.match(token)
                    if match is None:
                        continue

                    # group togheter all length-types
                    if token_family == 'length_2' or token_family == 'length_4':
                        token_family = 'length'

                    if token_family not in token_families:
                        token_families[token_family] = 1
                    token_families[token_family] += 1

                    if token_family == 'key':
                        token = re.search('\[K:(.+?)\]', token).group(1)
                        if token not in keys:
                            keys[token] = 1
                        keys[token] += 1

                    if token_family == 'meter':
                        token = re.search('\[M:(.+?)\]', token).group(1)
                        if token not in metrics:
                            metrics[token] = 1
                        metrics[token] += 1




        print(json.dumps(keys, sort_keys=True, indent=2))
        print(json.dumps(metrics, sort_keys=True, indent=2))
        print(json.dumps(token_families, sort_keys=True, indent=2))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--file',
        required=True,
        help='target file'
    )
    parser.add_argument(
        '-t',
        '--title',
        help='appends t to tile as \'Key distribution t\'',
        default=''
    )
    parser.add_argument(
        '-n',
        '--normalize',
        help='normalize values in graph',
        action='store_true',
    )
    args = parser.parse_args()
    analyze(args.file)
    plot_histogram(keys, args.normalize, 'Key distribution %s' % args.title)
    plot_histogram(metrics, args.normalize, 'Metric distribution %s' % args.title)
    plot_histogram(token_families, args.normalize, 'Token distribution %s' % args.title)
