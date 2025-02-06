import base64
import datetime
import server

# Tyler Brady and Madeline Park, Lab 1
# Contents: unmix function, left and right shift undo

# in server.py
# import unmix
# change current msg to "msg = web.ctx.env.get('HTTP_HOST') + unmix.reset_admin()" to admin part

def unmix(token_lst):
    # inverse of get_random_num (extract_number)
    state = []
    samples = []

    for t in token_lst:
        # each token is 8 list entries with colons
        stemp = base64.b64decode(t).split(b':')
        for a in stemp:
            samples.append(a)

    for sample in samples:
        # undo y ^= (y >> self.l)
        y = undo_right_shift(sample, server.MT.l)
        # undo y ^= (y << self.t) & self.c
        y = undo_left_shift(y, server.MT.t, server.MT.c)
        # undo y ^= (y << self.s) & self.b
        y = undo_left_shift(y, server.MT.s, server.MT.b)
        # undo y ^= (y >> self.u)
        y = undo_right_shift(y, server.MT.u)
        # add to new state list
        state.append(y)

    return state
    

def undo_right_shift(value, shift):
    W = server.MT.w
    res = value

    for i in range(0, W, shift):
        # preserve bits that are already the same with a mask
        # the 0s are where we want to recover the string
        # the 1s are already recovered parts we want to preserve        
        portion_mask = '0' * i + '1' * shift + '0' * (W - shift - i)
        portion_mask = int(portion_mask[:W], 2)
        # AND the original with part of the mask to preserve
        portion = int(res) & portion_mask
        # XOR with the part we preserved, shifted right by shift amount
        # anything XORed with 0 will be unchanged (restored bits)
        # and XORing with the shifted part will restore the original
        # because a ^ b = c, so a ^ c = b
        res = int(res) ^ int(portion >> shift)

    return res

def undo_left_shift(value, shift, mask):
    W = server.MT.w
    res = value
    for i in range(0, W, shift):
        # preserve bits that are already the same with a mask
        # the 0s are where we want to recover the string
        # the 1s are already recovered parts we want to preserve
        portion_mask = '0' * (W - shift - i) + '1' * shift + '0' * i
        portion_mask = int(portion_mask, 2)
        # AND the original value with the mask to preserve lower bits
        portion = int(res) & portion_mask

        # shift the portion by shift amount to shift upwards
        # AND with the mask to preserve restored data
        # XOR with original to restore
        res ^= ((portion << shift) & mask)

    return res

def reset_admin():
    token_lst = []
    for i in range(78):
        tok = server.generate_token()
        token_lst.append(tok)

    state_lst = unmix(token_lst)
    server.MT.state = state_lst
    token = server.generate_token()
    time = datetime.datetime.now() + datetime.timedelta(minutes=server.TIMEOUT)
    server.token_dic[token] = server.reset_token("admin", time)
    return "/reset?token=" + token.decode('utf-8')


