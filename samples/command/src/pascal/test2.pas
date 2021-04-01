unit Test2;

interface

function Test(n: Integer): Integer;

implementation

function Test(n: Integer): Integer;
begin
    writeln('Test2');
    Test := n * 10;
end;
end.
