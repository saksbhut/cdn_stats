

import json

import matplotlib
matplotlib.use
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Opening JSON file
    f = open('logs2.json', )

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    total_requests=0
    bytes_served_from_backend=0
    unique_urls_count=0
    cache_hit=0
    cache_miss=0
    unique_cacheid_count=0
    url_count={}
    unique_cacheid={}
    client_disconnected_after_partial_response=0
    client_disconnected_before_any_response=0
    #print(data[0]['httpRequest']['requestUrl'])
    for entry in data:
        total_requests+=1
        url=entry['httpRequest']['requestUrl']
        if url.find("?") == -1:
            print("No 'is' here!")
        cacheid=entry['jsonPayload']['cacheId']
        status_details=entry['jsonPayload']['statusDetails']
        if status_details=="response_sent_by_backend":
            cache_miss+=1
            if 'cacheFillBytes' in entry['httpRequest']:
                bytes_served_from_backend+=int(entry['httpRequest']['cacheFillBytes'])
        elif status_details=="response_from_cache":
            cache_hit+=1
        elif status_details=="client_disconnected_after_partial_response" :
            client_disconnected_after_partial_response+=1
        elif status_details=="client_disconnected_before_any_response":
            client_disconnected_before_any_response+=1


        if url not in url_count:
            unique_urls_count+=1
            url_count[url]=1
        else:
            url_count[url] +=1

        if cacheid not in unique_cacheid:
            unique_cacheid_count+=1
            unique_cacheid[cacheid]=1
        else:
            unique_cacheid[cacheid] +=1

    print("number of total requests",str(total_requests))
    print("client_disconnected_before_any_response",str(client_disconnected_before_any_response))
    print("client_disconnected_after_partial_response",str(client_disconnected_after_partial_response))
    print("number of cache hits",str(cache_hit))
    print("number of cache miss",str(cache_miss))
    print("total bytes served from the backend",str(bytes_served_from_backend))
    print ("cache hit ratio",str(cache_hit/total_requests))
    print("number of unique urls", str(unique_urls_count))
    print("number of unique cache locations used", str(unique_cacheid_count))

    import numpy as np

    fig, ax = plt.subplots(1, 1)
    a = list(url_count.values())
    my_bins=15
    arr=ax.hist(a, bins=15)
    for i in range(15):
        plt.text(arr[1][i], arr[0][i], str(arr[0][i]),fontsize=8)
    ax.set_title("histogram of result")
    ax.set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])

    #ax.set_xticks(range(len(my_bins) - 1))
    #plt.xticks(np.arange(min(x), max(x) + 1, 1.0))
    #ax.set_yticks([100, 200, 300,400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600,1700,1800,1900,2000])
    ax.set_xlabel('number of times a url is accessed')
    ax.set_ylabel('number of urls')
    plt.savefig('histogram.png')

    plt.figure(figsize=(30, 10))
    plt.bar(range(len(unique_cacheid)), list(unique_cacheid.values()), align='center')
    plt.xticks(range(len(unique_cacheid)), list(unique_cacheid.keys()))
    plt.title("Cache locations accessed")

    # # for python 2.x:
    # plt.bar(range(len(D)), D.values(), align='center')  # python 2.x
    # plt.xticks(range(len(D)), D.keys())  # in python 2.x

    plt.savefig('cachelocations.png')
    figureObject, axesObject = plt.subplots()
    # Draw the pie chart

    axesObject.pie(unique_cacheid.values(),

                   labels=unique_cacheid.keys(),

                   autopct='%1.2f',

                   startangle=90)

    # Aspect ratio - equal means pie is a circle

    axesObject.axis('equal')
    plt.title("Cache locations accessed")


    plt.savefig('cachepie.png')

    # Closing file
    f.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
