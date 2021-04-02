// This file is a "Hello, world!" in Pascal language by Free Pascal for wandbox.

{$I "config.inc"}

program Hello(output);

uses
    hoge in 'test2.pas',
    Test3;

begin
    writeln('Hello, Wandbox!');
    writeln({$I %DATE%});
    {$IF (Defined(TEST))}
    writeln('Test');
    {$ENDIF}
    {$INCLUDE 'test1.inc'}
    hoge.Test(10);
    Test3.Test3(10);
end.

// Free Pascal reference:
//   http://www.freepascal.org/

// Pascal language references:
//   http://www.gnu-pascal.de/gpc/
