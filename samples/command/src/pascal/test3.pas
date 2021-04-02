unit Test3;

interface

function Test3(n: Integer): Integer;

implementation

function Test3(n: Integer): Integer;
begin
    writeln('Test3');
    Test3 := n * 10;
end;
end.
