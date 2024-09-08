def retreive_experts():
    #{school:{name:expert_id}}
    expert_dict = {}
    for line in open('Experts.txt'):
        if 'Computer Science' in line:
            #Retreiving important values (school,name,expert_id)
            words = line.split('"')
            school_and_college = words[11].split(',')
            school = school_and_college[0]
            name = words[5] + " " + words[3]
            expert_id = words[1]
            
            #Adding expert dictionary to schools
            if school in expert_dict.keys():
                expert_dict[school][name] = expert_id
            else:
                expert_dict[school] = {name:expert_id}
                
    return expert_dict

def retreive_profiles(expert_dict):
    #{expert_id:[area_of_study]}
    profiles_dict = {}
    for line in open('Profiles.txt'):
        #Retreiving important values (expert_id,area_of_study)
        words = line.split('"')
        expert_id = words[1]
        area_of_study = words[5]
        
        #Add area of study
        #expert_id already exists in profiles_dict
        if expert_id in profiles_dict.keys():
            profiles_dict[expert_id].append(area_of_study)
            
        #expert_id doesn't exist in profile.dict
        else:
            for school in expert_dict:
                #Check if expert is in computer science 
                if expert_id in expert_dict[school].values():
                    profiles_dict[expert_id] = [area_of_study]
                
    return profiles_dict

def combine_dicts(expert_dict, profiles_dict):
    #{school:{name:[area_of_study]}}
    complete_dict = {}
    for school in expert_dict.keys():
        for name in expert_dict[school].keys():
            if expert_dict[school][name] in profiles_dict.keys():
                if school in complete_dict.keys():
                    complete_dict[school][name] = profiles_dict[expert_dict[school][name]]
                else:
                    complete_dict[school] = {name:profiles_dict[expert_dict[school][name]]}
    return complete_dict
        
def nc_scholar_system(complete_dict):
    cont = 'c'
    while cont == 'c':
        print('Welcome to the NC Scholar System')
        print('We are currently including scholars from the following institutes:')
        print(', '.join(complete_dict.keys()))
        print()
        school = input('Select an institute: ')
        if school in complete_dict.keys():
            print(school, 'has the following scholars in Computer Science:')
            for name in complete_dict[school].keys():
                print(name)
            print()
            area_of_study = input('Input an area of study: ')
            
            #Test if area of study is in dictionary and print it if it is
            test_aos = False
            for aos in complete_dict[school].values():
                if area_of_study in aos:
                    test_aos = True
            if test_aos:
                print(area_of_study, 'has the following scholars:')
                for name in complete_dict[school].keys():
                    if area_of_study in complete_dict[school][name]:
                        print(name)
                        
            #Test for simmilar areas of study if no one studies the area of study imput
            else:
                parts_of_aos = area_of_study.split(' ')
                first = True
                for name in complete_dict[school].keys():
                    best_fit = ''
                    best_num_of_hits = 0
                    for aos in complete_dict[school][name]:
                        num_of_hits = 0
                        for words in parts_of_aos:
                            if words in aos:
                                num_of_hits += 1
                                if first:
                                    print('There is no exact match, but we found some scholars that study similar areas:')
                                    print()
                                    first = False
                        if num_of_hits > best_num_of_hits:
                            best_num_of_hits = num_of_hits
                            best_fit = aos
                    if best_num_of_hits > 0:
                        print(name, '(' + best_fit + ')', end = '; ')
                        #print(name, complete_dict[school][name])
                    
                if first:
                    print('There is no one that studies', area_of_study)
                else:
                    print()
                    
            print()
            
        cont = input('Press c to continue or press anything else to quit: ')

if __name__ == '__main__':
    expert_dict = retreive_experts()
    profiles_dict = retreive_profiles(expert_dict)
    complete_dict = combine_dicts(expert_dict, profiles_dict)
    nc_scholar_system(complete_dict)
    