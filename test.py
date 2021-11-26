bars = 4
beats = 4
listabcd = ['a', 'b', 'c', 'd']
output = []

for bar in range(bars):
    for beat in range(beats):
        if bar % 4 == 0:
            output.append(listabcd[bar])
        output.append(beat)

for i in output:
    print(i)
