from OpenPose import OpenPose

# Example usage
def main():
    # File paths
    input_file = "test/PoseKeypoint3_00001.json"

    openpose_data = OpenPose.load(input_file)
        
    # guess the age, for fun
    print(openpose_data.people[0].guess_age()) 
    print(openpose_data.people[0].guess_gender()) 

if __name__ == "__main__":
    main()