def give_list_of_list(array, element):
    
    element = array[element]
    new_array = list(filter(lambda x: x!=element, array))
    return new_array


array = [[1,2],[2,3],[3,4],[4,5],[5,8]]


    
array = [ [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4] ]
remove_index = lambda index: lambda elem: elem != index
filtered_array = [ tuple(filter(remove_index(i+1), elem)) for i, elem in enumerate(array) ]
print(f"{filtered_array=}")