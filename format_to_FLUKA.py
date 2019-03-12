# FORMAT TO FLUKA

import utilities as ut
import logging

def FLUKA_output(input_file_name,output_file_name):
    
    df, maxlen = ut.read_excel(input_file_name)

    countdays = []
    countx = 0
    count0 = 0

    flux = []

    """ This loop extracts no. of days beam was on/off and flux amplitude from
        days it was on and appends it to the empty sets 'flux' and 'countdays'
    """
    for i in range(0, maxlen):
        if df[i] > 0 and (df[i]) == (df[i+1]):
            countx += 1
        elif df[i] > 0 and (df[i]) != (df[i+1]):
            countdays.append(countx)
            countx = 0
            flux.append(df[i])
        elif df[i] == 0 and (df[i]) == (df[i+1]):
            count0 += 1
        elif df[i] == 0 and (df[i]) != (df[i+1]):
            countdays.append(count0)
            count0 = 0
            flux.append(df[i])

    # convert days into seconds
    countdays = [x * 24 * 60 * 60 for x in countdays]
    countdays = [ut.round_to_sf(x,4) for x in countdays]
    
    
    flux = [ut.round_to_sf(x,4) for x in flux]
    flux = [ut.format_E(x,2) for x in flux]

    logging.debug(countdays)
    logging.debug(flux)

    logging.debug(type(flux[0]))
    logging.debug(type(flux[1]))

    tot = len(countdays)
    
    # write to FLUKA file

    with open(output_file_name, "w+") as file:
    # **** put something here to overwrite previous file ****
    
    # The conditionals are to satisfy FLUKAS input requirements.
    # These ensure beam flickers ON then OFF for corresponding values of flux

        for i in range(0, tot):  # could do step 3

        # write the comment lines. checking if have zero or non-zero flux
            if flux[i] == '0.0' and i % 3 == 2:  # end of line
                file.write("Beam OFF: "+str(countdays[i])+". seconds\n")
            elif flux[i] != '0.0' and i % 3 == 2: # end of line
                file.write("Beam ON: "+str(countdays[i])+". seconds\n")
            elif flux[i] == '0.0' and i % 3 == 0:  # beginning of line
                file.write("* Beam OFF: "+str(countdays[i])+". seconds,")
            elif flux[i] != '0.0' and i % 3 == 0:  # beginning of line
                file.write("* Beam ON: "+str(countdays[i])+". seconds,")
            elif flux[i] == '0.0': # middle of line
                file.write("Beam OFF: "+str(countdays[i])+". seconds,")
            elif flux[i] != '0.0': #middle of line 
                file.write("Beam ON: "+str(countdays[i])+". seconds,")

    
    # now write the IRRPROFI lines    
    file.close() 
    
    with open(output_file_name, "r+") as file:
        lines = file.readlines()
        #print('lines',lines)
        numlines = len(lines)
        logging.debug("THIS IS NUMLINES= %i", numlines)

        x = -3
        for j in range(0, numlines):
            x = x + 3
            if tot % 3 == 1 and x == tot - 1:  # end line, one value
                irrprofi = str("IRRPROFI"+(20 - (len(str(countdays[x]))+9))*" "
                           +str(countdays[x])+"."+(10-len(str(flux[x])))*" "
                           +str(flux[x]))
            elif tot % 3 == 2 and x == tot - 2:  # end line, two values
                 irrprofi = str("IRRPROFI"+(20 - (len(str(countdays[x]))+9))*" "
                           +str(countdays[x])+"."+(10-len(str(flux[x])))*" "
                           +str(flux[x])+(9-len(str(countdays[x+1])))*" "
                           +str(countdays[x+1])+"."+(10-len(str(flux[x+1])))*" "
                           +str(flux[x+1]))
            
            else:  # start and middle lines, 3 values per line
                irrprofi = str("IRRPROFI"+(20 - (len(str(countdays[x]))+9))*" "
                           +str(countdays[x])+"."+(10-len(str(flux[x])))*" "
                           +str(flux[x])+(9-len(str(countdays[x+1])))*" "
                           +str(countdays[x+1])+"."+(10-len(str(flux[x+1])))*" "
                           +str(flux[x+1])+(9-len(str(countdays[x+2])))*" "
                           +str(countdays[x+2]) +"."+(10-len(str(flux[x+2])))*" "
                           +str(flux[x+2])+"\n")
                
            lines.insert(2*j+1, irrprofi)

        lines = "".join(lines)
        file.seek(0)
        file.write(lines)
        file.truncate()
    file.close()


if __name__ == "__main__":
    input_file_name = 'cyclemainoperationalparameters.xlsx'
    output_file_name = 'fluka_test.i'
    ut.setup_logging()
    FLUKA_output(input_file_name,output_file_name)
    logging.info("Completed irradiation history production")
