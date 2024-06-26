本writeupはROP初心者向けを意識して作成しました。

## 分析
配布されたコードを見ると明らかにbofの脆弱性があります。
セキュリティ機構を調べると以下のようになります。
```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
Canaryも無効ですし、ROPを組んでシェルを取りましょう。

配布ファイルからも察しが付きますが、libc.so.6がリンクされています。
```
ubuntu@lima-ubuntu:~/Documents/archive/ctf4b2023/Elementary_ROP$ ldd chall
	linux-vdso.so.1 (0x00007fffcd7ca000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f4f01395000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f4f015c5000)
```

ついでにchallのガジェットを調べます。ROPgadgetを使いましょう。
しかし、challにはsystem関数は含まれません。
つまり、lib.so.6のsystemを使う必要があります。

しかし、libc.so.6はASLRが有効であるため、リンク先のアドレスはランダム化されてしまうので、共有ライブラリを用いるにはアドレスをリークさせる必要があります。

手法はいくつかありますが、今回はGOTからアドレスをリークさせます。
この手順を簡単に説明すると以下のようになります。
ここでは例としてputs関数を例に挙げます。
1. プログラムではputs関数が呼ばれると、PLTに対応するエントリにとぶ。
2. 最初の関数呼び出しでは、GOTが共有ライブラリのアドレスにしたがって更新される。これ以降の呼び出しではPLTはGOTを参照する。
3. GOTに格納されているアドレスをリークさせることで、puts関数の共有ライブラリ上のアドレスをリークさせることができる。

また、共有ライブラリ内のアドレスは保持される(共有ライブラリ内はランダムに変化しない)ため、リークしたアドレスと予め求められる共有ライブラリのオフセットを用いることで、共有ライブラリのアドレスをリークすることができます。
PLTやGOTについては、ぜひ詳しく調べてみてください。

これを念頭に置いて、challのディスアセンブリ結果を見ると、`printf@plt`が見つかります。0x401030を見るとわかるように、0x403fd0にprintf関数のアドレスを参照しています。
```
0000000000401030 <printf@plt>:
  401030:	ff 25 9a 2f 00 00    	jmp    *0x2f9a(%rip)        # 403fd0 <printf@GLIBC_2.2.5>
  401036:	68 00 00 00 00       	push   $0x0
  40103b:	e9 e0 ff ff ff       	jmp    401020 <_init+0x20>
```
つまり、このアドレスを出力させれば良いのです。

出力にはprintf関数がchallに含まれているので、これを用いれば良いです。引数として、このアドレスを与えてあげる必要があります。printf関数の第一引数に与えて呼び出せば良いのですが、これにはrdiレジスタに値を入れてprintfを呼び出せば良いです。
幸運にもpop rdiについては、src.cに書かれていますのでこれを使うことができます。

これで、libcのアドレスリークができるので、system関数を実行できます。しかし、いざアドレスを手に入れても、それを使って次のROP chainを作成して入力したいですが、このプログラムには入力の受付は1回しかありません。
このような時は、1回目のROP chainの最後にリターンアドレスをmain関数にしておき、再度main関数を実行させれば解決します。


## 方針
以上の分析から、本問題は以下の2つのchainを作成すれば良いです。
### 1つ目のchain
1. pop rdiにとばし、rdiに入れる用の値をスタックに入れておく。
2. printfにとばす。
3. mainにとばす。

### 2つ目のchain
(出力されたアドレスからlibcのベースアドレスを計算する)
1. libcからsystem("/bin/sh")を実行させる
