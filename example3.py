from OpenPose import OpenPose

# Example usage
def main():
    # File paths
    input_file = "Adult_woman_dancing.json"

    output_prefix = "Adult_woman_dancing_scaled_to_girl_age"
    target_gender = "female"

    for target_age in (4,6,8,10,12,14,16):
        openpose_data = OpenPose.load(input_file)
        
        # guess the age, for fun
        print(openpose_data.people[0].guess_age()) 
        
        #guise the algorithm with correct input data
        openpose_data.people[0].input_age = 20
        openpose_data.people[0].input_gender = "female"

        for index, pose in enumerate(openpose_data.people):
            print(f"Scaling pose {index} to target age {target_age} and gender {target_gender}.")

            openpose_data.scale_pose(index, target_gender=target_gender, target_age=target_age) # MAGIC!

            file_name = f"{output_prefix}_{target_age}"
            openpose_data.save(f"{file_name}.json")
            openpose_data.save_as_image(f"{file_name}.png")

if __name__ == "__main__":
    main()