import os
import rand

# we get the absolute file path, otherwise relative filepath would work only from certain working directory
# downside is that if we move any of the files, this will silently break
dirname = os.path.dirname(__file__)
data_filepath = os.path.join(dirname, '../podatki/complete.csv')

# DATA COLUMNS IN ORDER
# datetime,city,state,country,shape,duration (seconds),duration (hours/min),comments,date posted,latitude,longitude

# here we add in our existing ufo data we got from kaggle
# assume, we have some placeholder users already defined in the db
# and randomly assign them the ufo sightings as if they were theirs
# for the sake of making a demo project
with open(data_filepath) as F:
    lines = [x.strip() for x in F.readlines()]
    print(lines[0])
    print(lines[1])
    print(lines[2])


    queries = []

    for line in lines[1:2]:
        # SIGHTINGS COLUMNS IN ORDER
        # title, sighting_date, description, coords, duration, user_id, creation_date 
        title = f"Sighting of {line[4]}-shaped UFO in {line[1].capitalize()}, {line[2].capitalize()}"
        coords = f"({line[9]}, {line[10]})"
        
        query = f"""INSERT INTO SIGHTINGS VALUES (
            {title},
            {line[0]},
            {line[7]},
            {coords},
            {line[5]},
            {random.randint(1, 10)},
            {line[8]}
        )
        """
