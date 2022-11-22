def get_best_protein():
    data_dict = {}
    dist_dict = {}

    with open('text/summary.txt', 'r') as summary:
        write = False
        for line in summary:

            if line == 'Founded Domains:\n':
                write = True
                continue

            elif line == 'Info from Uniprot:\n':
                break

            if write:
                data_list = line.strip().split(' ', 1)
                domain_list = data_list[1].strip().split(' ')
                domain_list_refined = []

                total_dist = 0
                for domain in domain_list:
                    domain = domain.split(',')
                    domain_refined = []
                    for area in domain:
                        area = area.split('-')
                        area = list(map(int, area))
                        area.sort()
                        print(area)

                        domain_refined.append(area)

                    for dist in domain:
                        dist = abs(eval(dist))
                        total_dist += dist

                    domain_list_refined.append(domain_refined)

                dist_dict[data_list[0]] = total_dist
                data_dict[data_list[0]] = domain_list_refined

        best_cov = max(dist_dict, key=dist_dict.get)

    return best_cov, data_dict[best_cov]
