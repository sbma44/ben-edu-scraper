 # -*- coding: utf-8 -*-

import __future__
import sys, csv, re, hashlib

def strip_tags(x):
    return re.sub(r'<\/?[^>]+>', '', x)

def main():
    writer = csv.writer(sys.stdout)
    out = {}
    with open(sys.argv[1]) as f:

        # initialize variables
        record = []
        headers = []
        name = ''
        founded = ''
        pubpriv = ''

        for line in f:
            # strip whitespace
            line = line.strip()

            # if this is a header line, store it
            m = re.search(r'<th align="CENTER"><span style="text-decoration:underline;">(.*?)</span></th>', line)
            if m is not None:
                headers.append(m.group(1))

            # if this is a title line, break it up & store the parts
            m = re.search(r'<h4><a name="(?P<shortname>[^"]+)"></a>(?P<name>.*?) – (?P<pubpriv>.*?) – FOUNDED/ACCREDITED: (?P<founded>\d+)/(?P<accredited>\d+)</h4>', line)
            if m is not None:
                name = m.group('name')
                founded = m.group('founded')
                accredited = m.group('accredited')
                pubpriv = m.group('pubpriv')

            # begin collecting a new row when </tr> is found
            if line == '</tr>':
                record.append([])

            # data cell? append it
            m = re.search(r'<td align="CENTER">(.*?)<\/td>', line)
            if m is not None:
                record[-1].append(strip_tags(m.group(1)))

            # asterisks show up between records; emit what we have,
            # reset everything & start collecting again
            if '**********' in line:
                h = hashlib.md5('|'.join(headers)).hexdigest()
                if not h in out:
                    out[h] = {
                        'headers': ['NAME', 'FOUNDED', 'ACCREDITED', 'PUB/PRIV'] + headers,
                        'rows': []
                    }
                for r in record:
                    if len(r):
                        out[h]['rows'].append([name, founded, accredited, pubpriv] + r)

                record = []
                headers = []
                name = ''
                founded = ''
                pubpriv = ''

    # emit results
    for h in out:
        with open('{}.csv'.format(h), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(out[h]['headers'])
            for row in out[h]['rows']:
                writer.writerow(row)

if __name__ == '__main__':
    main()