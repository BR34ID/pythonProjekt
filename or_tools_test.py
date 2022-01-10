from ortools.constraint_solver import pywrapcp, routing_enums_pb2

solution_nodes = []

def create_data_model(distance_matrix):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = distance_matrix
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

def distance_callback(from_index, to_index):
    """Returns the distance between the two nodes."""
    # Convert from routing variable Index to distance matrix NodeIndex.
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data['distance_matrix'][from_node][to_node]

def print_solution(manager, routing, solution, addresses):
    """Prints solution on console."""
    #print('Objective: {} miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route:\n'
    route_distance = 0
    solution_nodes.clear()
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(addresses[manager.IndexToNode(index)])
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        solution_nodes.append(manager.IndexToNode(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(addresses[manager.IndexToNode(index)])
    plan_output += 'Distanz: {} km\n'.format(route_distance/1000)
    print(plan_output)
    print(solution_nodes)

def getSolution(addresses, distance_matrix):
    global data, manager
    data = create_data_model(distance_matrix)
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        print_solution(manager, routing, solution, addresses)