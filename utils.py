def mask_ip(ip):
    ip = ip.split('.')[::-1]
    masked_ip = ''
    for i in range(len(ip)):
        masked_ip += str((255 - int(ip[i]) + i))
        if i < len(ip) - 1:
            masked_ip += '.'

    return masked_ip

def decode_mask_ip(ip):
    ip = ip.split('.')[::-1]
    masked_ip = ''
    for i in range(len(ip)):
        masked_ip += str((255 - int(ip[i]) + (len(ip) - i - 1)))
        if i < len(ip) - 1:
            masked_ip += '.'

    return masked_ip

def mask_device_id(device_id):
    device_id = device_id[::-1]
    mask_device_id = ''
    for i in range(len(device_id)):
        if device_id[i].isdigit():
            mask_device_id += str(chr(int(device_id[i]) + 65))
        else:
            mask_device_id += '-'

    return mask_device_id

def decode_device_id(device_id):
    device_id = device_id[::-1]
    mask_device_id = ''
    for i in range(len(device_id)):
        if device_id[i].isalpha():
            mask_device_id += str(ord(device_id[i]) - 65)
        else:
            mask_device_id += '-'

    return mask_device_id

if __name__ == "__main__":
    print(mask_ip('192.168.0.1'))
    print(decode_mask_ip(mask_ip('192.168.0.1')))