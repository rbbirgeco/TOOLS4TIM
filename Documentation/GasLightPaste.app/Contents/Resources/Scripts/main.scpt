FasdUAS 1.101.10   ��   ��    k             l     ��  ��    , & Get current date and format timestamp     � 	 	 L   G e t   c u r r e n t   d a t e   a n d   f o r m a t   t i m e s t a m p   
  
 l     ����  r         I    ������
�� .misccurdldt    ��� null��  ��    o      ���� 0 currentdate currentDate��  ��        l    ����  r        n        7   ��  
�� 
ctxt  m    ������  m    ������  l    ����  b        m    	   �    0  l  	  ����  c   	     n   	    !   1   
 ��
�� 
year ! o   	 
���� 0 currentdate currentDate  m    ��
�� 
TEXT��  ��  ��  ��    o      ���� 0 yearstr yearStr��  ��     " # " l   1 $���� $ r    1 % & % n    / ' ( ' 7  % /�� ) *
�� 
ctxt ) m   ) +������ * m   , .������ ( l   % +���� + b    % , - , m     . . � / /  0 - l   $ 0���� 0 c    $ 1 2 1 l   " 3���� 3 c    " 4 5 4 n      6 7 6 m     ��
�� 
mnth 7 o    ���� 0 currentdate currentDate 5 m     !��
�� 
long��  ��   2 m   " #��
�� 
TEXT��  ��  ��  ��   & o      ���� 0 monthstr monthStr��  ��   #  8 9 8 l  2 E :���� : r   2 E ; < ; n   2 C = > = 7  9 C�� ? @
�� 
ctxt ? m   = ?������ @ m   @ B������ > l  2 9 A���� A b   2 9 B C B m   2 3 D D � E E  0 C l  3 8 F���� F c   3 8 G H G n   3 6 I J I 1   4 6��
�� 
day  J o   3 4���� 0 currentdate currentDate H m   6 7��
�� 
TEXT��  ��  ��  ��   < o      ���� 0 daystr dayStr��  ��   9  K L K l  F ] M���� M r   F ] N O N n   F Y P Q P 7  O Y�� R S
�� 
ctxt R m   S U������ S m   V X������ Q l  F O T���� T b   F O U V U m   F G W W � X X  0 V l  G N Y���� Y c   G N Z [ Z n   G L \ ] \ 1   H L��
�� 
hour ] o   G H���� 0 currentdate currentDate [ m   L M��
�� 
TEXT��  ��  ��  ��   O o      ���� 0 hourstr hourStr��  ��   L  ^ _ ^ l  ^ w `���� ` r   ^ w a b a n   ^ s c d c 7  i s�� e f
�� 
ctxt e m   m o������ f m   p r������ d l  ^ i g���� g b   ^ i h i h m   ^ a j j � k k  0 i l  a h l���� l c   a h m n m n   a f o p o 1   b f��
�� 
min  p o   a b���� 0 currentdate currentDate n m   f g��
�� 
TEXT��  ��  ��  ��   b o      ���� 0 	minutestr 	minuteStr��  ��   _  q r q l  x � s���� s r   x � t u t n   x � v w v 7  � ��� x y
�� 
ctxt x m   � ������� y m   � ������� w l  x � z���� z b   x � { | { m   x { } } � ~ ~  0 | l  { � ����  c   { � � � � n   { � � � � m   | ���
�� 
scnd � o   { |���� 0 currentdate currentDate � m   � ���
�� 
TEXT��  ��  ��  ��   u o      ���� 0 	secondstr 	secondStr��  ��   r  � � � l     ��������  ��  ��   �  � � � l     �� � ���   �   Build filename    � � � �    B u i l d   f i l e n a m e �  � � � l  � � ����� � r   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � o   � ����� 0 yearstr yearStr � o   � ����� 0 monthstr monthStr � o   � ����� 0 daystr dayStr � m   � � � � � � �  _ � o   � ����� 0 hourstr hourStr � o   � ����� 0 	minutestr 	minuteStr � o   � ����� 0 	secondstr 	secondStr � m   � � � � � � �  G A S L I G H T _ L O G � m   � � � � � � �  . m d � o      ���� 0 filename fileName��  ��   �  � � � l     ��������  ��  ��   �  � � � l     �� � ���   � * $ Get path to folder the script is in    � � � � H   G e t   p a t h   t o   f o l d e r   t h e   s c r i p t   i s   i n �  � � � l  � � ����� � r   � � � � � n   � � � � � 1   � ���
�� 
psxp � l  � � ����� � I  � ��� ���
�� .earsffdralis        afdr �  f   � ���  ��  ��   � o      ���� 0 
scriptpath 
scriptPath��  ��   �  � � � l  � � ����� � r   � � � � � I  � ��� ���
�� .sysoexecTEXT���     TEXT � b   � � � � � m   � � � � � � �  d i r n a m e   � n   � � � � � 1   � ���
�� 
strq � o   � ����� 0 
scriptpath 
scriptPath��   � o      ���� 0 
folderpath 
folderPath��  ��   �  � � � l  � � ����� � r   � � � � � b   � � � � � b   � � � � � o   � ����� 0 
folderpath 
folderPath � m   � � � � � � �  / � o   � ����� 0 filename fileName � o      ���� 0 fullpath fullPath��  ��   �  � � � l     �������  ��  �   �  � � � l     �~ � ��~   �   Get clipboard contents    � � � � .   G e t   c l i p b o a r d   c o n t e n t s �  � � � l  � � ��}�| � r   � � � � � I  � ��{�z�y
�{ .JonsgClp****    ��� null�z  �y   � o      �x�x 0 clipcontents clipContents�}  �|   �  � � � l     �w�v�u�w  �v  �u   �  � � � l     �t � ��t   � !  Write contents to new file    � � � � 6   W r i t e   c o n t e n t s   t o   n e w   f i l e �  ��s � l  � ��r�q � I  ��p ��o
�p .sysoexecTEXT���     TEXT � b   � � � � b   � � � � � b   � � � � � m   � � � � � � � 
 e c h o   � n   � � � � � 1   � ��n
�n 
strq � o   � ��m�m 0 clipcontents clipContents � m   � � � � � � �    >   � n   � � � � 1  �l
�l 
strq � o   ��k�k 0 fullpath fullPath�o  �r  �q  �s       �j � ��j   � �i
�i .aevtoappnull  �   � **** � �h ��g�f � ��e
�h .aevtoappnull  �   � **** � k     � �  
 � �   � �  " � �  8 � �  K � �  ^ � �  q � �  � � �  � � �  �    �  �  ��d�d  �g  �f   �   � )�c�b �a�`�_�^�] .�\�[�Z D�Y�X W�W�V j�U�T }�S�R � � ��Q�P�O�N ��M�L�K ��J�I�H � �
�c .misccurdldt    ��� null�b 0 currentdate currentDate
�a 
year
�` 
TEXT
�_ 
ctxt�^���] 0 yearstr yearStr
�\ 
mnth
�[ 
long�Z 0 monthstr monthStr
�Y 
day �X 0 daystr dayStr
�W 
hour�V 0 hourstr hourStr
�U 
min �T 0 	minutestr 	minuteStr
�S 
scnd�R 0 	secondstr 	secondStr�Q 0 filename fileName
�P .earsffdralis        afdr
�O 
psxp�N 0 
scriptpath 
scriptPath
�M 
strq
�L .sysoexecTEXT���     TEXT�K 0 
folderpath 
folderPath�J 0 fullpath fullPath
�I .JonsgClp****    ��� null�H 0 clipcontents clipContents�e*j  E�O���,�&%[�\[Z�\Zi2E�O���,�&�&%[�\[Z�\Zi2E�O���,�&%[�\[Z�\Zi2E�O��a ,�&%[�\[Z�\Zi2E` Oa �a ,�&%[�\[Z�\Zi2E` Oa �a ,�&%[�\[Z�\Zi2E` O��%�%a %_ %_ %_ %a %a %E` O)j a ,E` Oa _ a  ,%j !E` "O_ "a #%_ %E` $O*j %E` &Oa '_ &a  ,%a (%_ $a  ,%j ! ascr  ��ޭ