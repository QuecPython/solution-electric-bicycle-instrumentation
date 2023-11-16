# Copyright (c) Quectel Wireless Solution, Co., Ltd.All Rights Reserved.
 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
 
#     http://www.apache.org/licenses/LICENSE-2.0
 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: UTF-8 -*-
import ucryptolib
import ujson
from usr.utils.log import log

def encrypt(data: bytes, key: bytes, padding=16):
    paddata = pad(data, padding)
    log.d('paddata', paddata)
    encrypted_data = aes_encrypt(paddata, key[:16])
    log.d('encrypted_data', encrypted_data)
    return encrypted_data
    
def decrypt(data: bytes, key: bytes, padding=16):
    log.d('decrypt data:', data)
    log.d('decrypt key:', key)
    undecrypt_data = aes_decrypt(data, key[:16])
    log.d('undecrypt_data:', undecrypt_data)
    unpadded_data = unpad(undecrypt_data, padding)
    log.d('unpadded_data:', unpadded_data)
    # jsondata = ujson.load(unpadded_data)
    # log.d('jsondata:', jsondata)
    return unpadded_data

def aes_decrypt(data: bytes, eKey: bytes):
    aes = ucryptolib.aes(eKey, 1)
    rawdata = aes.decrypt(data)
    return rawdata
    
def aes_encrypt(data: bytes, eKey: bytes):
    aes = ucryptolib.aes(eKey, 1)
    encrypt_data = aes.encrypt(data)
    return encrypt_data

def bchr(ch):
    return chr(ch).encode('utf-8')

def pad(data_to_pad, block_size, style='pkcs7'):
    padding_len = block_size-len(data_to_pad)%block_size
    if style == 'pkcs7':
        padding = bchr(padding_len)*padding_len
    elif style == 'x923':
        padding = bchr(0)*(padding_len-1) + bchr(padding_len)
    elif style == 'iso7816':
        padding = bchr(128) + bchr(0)*(padding_len-1)
    else:
        raise ValueError("Unknown padding style")
    return data_to_pad + padding


def unpad(padded_data, block_size, style='pkcs7'):
    pdata_len = len(padded_data)
    log.d('unpad len : ', pdata_len)
    if pdata_len == 0:
        raise ValueError("Zero-length input cannot be unpadded")
    if pdata_len % block_size:
        log.d('Input data is not padded')
        raise ValueError("Input data is not padded")
    if style in ('pkcs7', 'x923'):
        padding_len = padded_data[-1]
        if padding_len<1 or padding_len>min(block_size, pdata_len):
            log.d('Padding is incorrect.')
            # raise ValueError("Padding is incorrect.")
            return padded_data
        if style == 'pkcs7':
            if padded_data[-padding_len:]!=bchr(padding_len)*padding_len:
                log.d('PKCS#7 padding is incorrect.')
                # raise ValueError("PKCS#7 padding is incorrect.")
                return padded_data
        else:
            if padded_data[-padding_len:-1]!=bchr(0)*(padding_len-1):
                # raise ValueError("ANSI X.923 padding is incorrect.")
                return padded_data
    elif style == 'iso7816':
        padding_len = pdata_len - padded_data.rfind(bchr(128))
        if padding_len<1 or padding_len>min(block_size, pdata_len):
            raise ValueError("Padding is incorrect.")
        if padding_len>1 and padded_data[1-padding_len:]!=bchr(0)*(padding_len-1):
            raise ValueError("ISO 7816-4 padding is incorrect.")
    else:
        raise ValueError("Unknown padding style")
    return padded_data[:-padding_len]
    
if __name__ == '__main__':
    rawdata = b'asdfasdf'
    key = b'1111111111111111'
    print('rawdata', rawdata)
    paddata = pad(rawdata, 16)
    print('padded', paddata)
    encrypted_data = aes_encrypt(paddata, key)
    print('encrypted', encrypted_data)
    rawdata2 = aes_decrypt(encrypted_data, key)
    print('decrypted', rawdata2)
    unpaddeddata = unpad(rawdata2, 16)
    print('unpadded', unpaddeddata)
    plaintext = unpaddeddata.decode('utf-8')
    print('final', plaintext)
