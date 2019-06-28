# Lucky 13

Lucky 13 is a full plaintext recovery attack for TLS and DTLS protocols. 
It was proposed by Nadhem J. AlFardan and Kenneth G. Paterson on their paper 
_Lucky Thirteen: Breaking the TLS and DTLS Record Protocols_.

## Implementation

This implementation of Lucky 13 works using a _Cheating Oracle_ instead of 
measuring the response time, as it was explained on the paper. This oracle 
looks directly at the decrypted values to find the correct padding.  

It works using a block size of 16 bytes and a MAC size of 20. That can be changed
on the constants file, though the TLS simulator should be changed as well. 

## Usage

To use this, simply run the script \_\_main__.py and enter the message when prompted.
The recovered text will be displayed on screen, along with the MAC tag and 
 the padding, once finished. 