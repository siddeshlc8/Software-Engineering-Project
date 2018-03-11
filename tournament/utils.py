def rr_schedule(n):
    slots = []

    n = int(n)

    for i in range(1, 2 * n):
        match = []
        match.append([i, 2*n])
        for x in range(1, 2 * n):
            for y in range(1, 2 * n):
                if x != y:
                    if [y,x] not in match:
                        if ((x + y) - 2 * i) % ((2 * n) - 1) == 0:
                            match.append([x, y])
        slots.append(match)
    '''
    #j = 1
    #for slot in slots:
        #print('----------SLOT-' + str(j) + '------------')
        #j = j + 1
        #for match in slot:
            #print(match)
    '''

    return slots
