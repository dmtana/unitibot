# SPECS 
adjustment      = 0.33

gap_last_piece  = 4

S = 93  -adjustment
M = 135 -adjustment
L = 199 -adjustment

# sample_line     = 'LMSMLMMSLMLLSMLMLSML'

def calc_(sample_line, panel_width):
    panel_width=int(panel_width)
    ans_str=''
    c = 0
    for sample in sample_line[::-1]:
        if sample == 'L':
            if c+L < panel_width:
                c=c+L
            else:
                print('L sample is too big for panel width')    
                break
        if sample == 'S':
            if c+S < panel_width:    
                c=c+S 
            else:
                print('S sample is too big for panel width')    
                break        
        if sample == 'M':
            if c+M < panel_width:
                c=c+M
            else:
                print('M sample is too big for panel width')    
                break     
        try: 
            ans_str+=str(round(panel_width-c))+'\n'
        except Exception:
            print('ERR')
    try:
        ans_str+=('\n'+'last piece is '+f'{round(panel_width-c-4)}'+'mm cut length')
    except Exception:
        print('ERR2')
    return ans_str

# TEST 
# result = calc_('LMSMLMMSLMLLSMLMLSML', '3000')
# print(result)

