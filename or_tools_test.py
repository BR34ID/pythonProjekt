from ortools.constraint_solver import pywrapcp, routing_enums_pb2

class Solver:
    def __init__(self, distanceMatrixGenerator):
        self.solution_nodes = []
        self.distanceMatrixGenerator = distanceMatrixGenerator
        self.distanceMatrix = self.distanceMatrixGenerator.generate_distance_matrix()
        self.data_model = {('distance_matrix', self.distanceMatrix), ('num_vehicles', 1), ('depot', 0)}
        self.manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
        self.routing = pywrapcp.RoutingModel(manager)
        transit_callback_index = self.routing.RegisterTransitCallback(self.distance_callback)
        self.routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        self.search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        self.search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    def distance_callback(self, from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = self.manager.IndexToNode(from_index)
        to_node = self.manager.IndexToNode(to_index)
        return self.data['distance_matrix'][from_node][to_node]

    def print_solution(self, manager, routing, solution):
        """Prints solution on console."""
        index = routing.Start(0)
        plan_output = 'Route:\n'
        route_distance = 0
        self.solution_nodes.clear()
        while not routing.IsEnd(index):
            plan_output += ' {} ->'.format(self.distanceMatrixGenerator.getAdresses()[manager.IndexToNode(index)])
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            self.solution_nodes.append(manager.IndexToNode(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        plan_output += ' {}\n'.format(self.distanceMatrixGenerator.getAdresses()[manager.IndexToNode(index)])
        plan_output += 'Distanz: {} km\n'.format(route_distance/1000)
        print(plan_output)
        print(self.solution_nodes)

    def getSolution(self):
        solution = self.routing.SolveWithParameters(self.search_parameters)
        if solution:
            self.print_solution(self.manager, self.routing, solution, self.distanceMatrixGenerator)

    def getSolutionNodes(self):
        return self.solution_nodes