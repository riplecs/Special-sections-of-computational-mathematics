## LABA1 : long arithmetic

The following operations were implemented:

- adding numbers;
- subtraction of numbers;
- multiplication of numbers, raising numbers to the square;
- division of numbers, finding the remainder of the division;
- raising the number to a multi-digit degree;
- conversion (translation) of a number into a character string and inverse conversion character string in number;

There also were released: 
1. calculation of GCD and LCM of two numbers;
2. adding numbers modulo;
3. subtraction of numbers modulo;
4. multiplication of numbers and subtraction of numbers to the square modulo;
5. raising the number to multi-digit power d modulo n.

Modular arithmetic was implemented on the basis of Barrett's reduction, exaltation to the degree - based on the Horner scheme.

## LABA2 : Implementation of operations in finite fields of characteristic 2

Was implemented a Galois field of characteristic 2 of degree m in the polynomial and normal basises:
1. adding elements;
2. multiplication of elements;
3. calculation of the trace element;
4. elevation of the field element to the square;
5. elevation of the field element to an arbitrary degree (not more than 2^m-1, where m is dimension of expansion);
6. finding the inverse element by multiplication;
7. conversion (translation) of a field element into an m-bit (string image) and vice versa, where m is the dimension of the extension;
