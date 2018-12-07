import argparse
import re
import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import savemat

keys = {}
metrics = {}
token_families = {}
line_structure = {}
notes = {}
song_token_counts = {}

def sort_by_label(data):
    labels = []
    values = []
    for key, val in data.items():
        labels.append(key)
        values.append(val)
    values = [v for _,v in sorted(zip(labels, values))]
    labels = sorted(labels)
    return labels, values

def plot_histogram(data, normalize, title):
    labels, values = sort_by_label(data)

    values = np.array(values).astype(float)
    if normalize:
        values /= np.sum(values)

    plt.title(title)
    plt.bar(np.arange(len(labels)), values)
    plt.xticks(np.arange(len(labels)), labels, rotation=70)
    plt.show()

def convert_to_mat(filename):

    keys_labels, keys_values = sort_by_label(keys)
    metrics_labels, metrics_values = sort_by_label(metrics)
    token_labels, token_values = sort_by_label(token_families)
    note_label, note_value = sort_by_label(notes)
    count_label, count_value = sort_by_label(song_token_counts)
    savemat(filename, {
        'keys_l': keys_labels,
        'keys_v': keys_values,
        'metrics_l': metrics_labels,
        'metrics_v': metrics_values,
        'token_l': token_labels,
        'token_v': token_values,
        'note_l': note_label,
        'note_v': note_value,
        'count_l': count_label,
        'count_v': count_value
    })

def analyze(filename, structures):

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
    re_error = re.compile(r".+")
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
            'length_4': re_length_short_4,
            'error': re_error
            }

    with open(filename, 'r') as f:
        token_count = 0
        expected_token_count = 0
        T = []
        text = []
        for line in f:
            text = f.read()
        songs = text.split('\n\n')


        for line in songs:
            tokens = line.split()
            # Remove X:0 from bobs transcripts
            if len(tokens) > 0:
                if re.match(r"X:\d+", tokens[0]):
                    del tokens[0]

                l = len(tokens)
                if l not in song_token_counts:
                    song_token_counts[l] = 0
                song_token_counts[l] += 1


                structure = ''
                struct_check = False
                for token in tokens:
                    expected_token_count += 1
                    for token_family, reg in regex_dict.items():
                        match = reg.match(token)
                        if match is None:
                            continue
                        token_count += 1


                        if structures:
                            if token_family == 'bar' or token_family == 'repeat':
                                struct_check = True
                                structure += token + ' '

                        # group togheter all length-types
                        #if token_family == 'length_2' or token_family == 'length_4':
                        #    token_family = 'length'

                        if token_family == 'error':
                            print(token)

                        if token_family not in token_families:
                            token_families[token_family] = 0
                        token_families[token_family] += 1

                        if token_family == 'key':
                            token = re.search('\[K:(.+?)\]', token).group(1)
                            if token not in keys:
                                keys[token] = 0
                            keys[token] += 1

                        if token_family == 'meter':
                            token = re.search('\[M:(.+?)\]', token).group(1)
                            if token not in metrics:
                                metrics[token] = 0
                            metrics[token] += 1

                        if token_family == 'note':
                            if token not in notes:
                                notes[token] = 0
                            notes[token] += 1

                        break

                if len(structure) > 0:
                    if structure not in line_structure:
                        line_structure[structure] = 1
                    line_structure[structure] += 1

        print(json.dumps(keys, sort_keys=True, indent=2))
        print(json.dumps(metrics, sort_keys=True, indent=2))
        print(json.dumps(token_families, sort_keys=True, indent=2))
        print(json.dumps(song_token_counts, sort_keys=True, indent=2))
        print(json.dumps(notes, sort_keys=True, indent=2))
        print('Tokens found: {} of {} ({:.3f}%)'.format(token_count, expected_token_count, float(token_count/expected_token_count)*100))

        if structures:
            print('Top {} line structures'.format(structures))
            print('ID\tCOUNT\tSTRUCTURE')
            id = 1
            for structure, count in reversed(sorted(line_structure.items(), key=lambda kv: kv[1])):
                print(f'{id}\t{count}\t{structure}')
                id += 1
                if id > int(structures):
                    break


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
    parser.add_argument(
        '-om',
        '--output_matlab',
        required=False,
        help='output summary to ./path/of/filename.mat',
        default=None,
    )
    parser.add_argument(
        '--line_structure',
        help='parses for top number of measure line structures',
        default=False
    )
    args = parser.parse_args()
    analyze(args.file, args.line_structure)

    if args.output_matlab:
        convert_to_mat(args.output_matlab)
    else:
        #plot_histogram(keys, args.normalize, 'Key distribution %s' % args.title)
        #plot_histogram(metrics, args.normalize, 'Metric distribution %s' % args.title)
        #plot_histogram(token_families, args.normalize, 'Token distribution %s' % args.title)
        pass
