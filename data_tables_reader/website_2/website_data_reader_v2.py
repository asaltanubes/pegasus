import numpy as np

#  TUve que editar el file del planeta PLuto, porque tiene un formato distinto.
#  Y no hay masa para el cometa halley :(
# 

def read_files(number_of_files):
    output_file_name = './data_tables_reader/initial_conditions.ini'
    with open(output_file_name, 'w')  as file:
        file.truncate(0)
        file.write('# Name, x, y, z, vx, vy, vz DATE------ on last line\n')
    for i in range(0,number_of_files):
        file_name:str = f'./data_tables_reader/website_2/web_data/horizons_results ({i}).txt'
        with open(file_name) as f:
            lines = f.readlines() 
            # cond = True # para la masa 
            for n, line in enumerate(lines):           
                if ' '.join(line.split(' ')[0:3]).strip().lower() == 'target body name:':
                    astro_name = line.split(' ')[3].strip().lower()

                if ' '.join(line.split(' ')).strip().lower() == '$$soe':
                    marker_position = n 

                # if 'mass' in line.lower() and cond == True:
                #     cond = False
                #     marker_mass = n
                #     print(line)
                #     try:
                #         index_mass = line.lower().split('\t').index('mass')
                #     except: 
                #         index_mass = line.lower().split('\t').index('mass,')
                #         pass
                #     print(index_mass)
                #     # index_mass = lines[n].split('\t').index('mass')
                #     # mass_line = lines[n].split(' ')[index_mass, lines[marker_mass].split(' ').index()+2]
                #     # print(mass_line)
            date_line = lines[marker_position+1]
            position_line = lines[marker_position+2].split('=')
            velocity_line = lines[marker_position+3].split('=')
            # mass_line = lines[marker_mass].split(' ').index()
            position = [position_line[1].strip().split(' ')[0].strip(),
                        position_line[2].strip().split(' ')[0].strip(),
                        position_line[3].strip().split('\n')[0].strip()]
            velocity = [velocity_line[1].strip().split(' ')[0].strip(),
                    velocity_line[2].strip().split(' ')[0].strip(),
                    velocity_line[3].strip().split('\n')[0].strip()]
            f.close()
        # print(date_line)
        # print(astro_name)
        # print(position) 
        # print(velocity)
        with open(output_file_name, 'a')  as file:
            file.write(f'{astro_name},\t{',\t'.join([str(i) for i in position])},\t{',\t'.join([str(i) for i in velocity])},\n')
    with open(output_file_name, 'a')  as file:
        file.write('#\t'+ date_line + '\n')
    


read_files(11)