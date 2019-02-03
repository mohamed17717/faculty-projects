def binary_search(lst, elm):
  ## must be sorted lst cus its depends on midian (basic statistics)
  lst.sort()

  while lst:
    ## to tell you howmany loops happened (not neccesary)
    print(lst)

    ## midian
    length   = len(lst)
    midIndex = length // 2
    mid      = lst[midIndex]

    ## cretical points
    if elm == mid or length == 1:
      break

    ## searched elm must be in right part
    elif elm > mid:
      ## index + 1 because already compared to mid and not matched
      lst = lst[midIndex+1:]

    ## searched elm must be in left part
    elif elm < mid:
      lst = lst[:midIndex]

  return elm == mid

#from sys import argv
#lst = [1,71,24,5,8,75,41,7,50,14,4,69]
#elm = int(argv[1])
#print(binary_search(lst, elm))
