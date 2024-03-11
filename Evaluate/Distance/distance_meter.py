def calculate_distance_manhattan(init_point, end_point):
    return (
        
            abs(init_point.coordinate_x - end_point.coordinate_x) 
            + abs(init_point.coordinate_y - end_point.coordinate_y)
        
        )