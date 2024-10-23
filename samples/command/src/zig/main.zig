const std = @import("std");
const test1 = @import("test1.zig");
const test2 = @import("./test2.zig").print;
const test3 = @import("sub/test3.zig").print;
const test4 = @import("sub/test4.zig");
const test5 = @import("sub/test5/test5.zig").print; const root_print = @import("root").print_all;

pub fn main() void {
    std.debug.print("Hello, {s}!\n", .{"World"});
    root_print();
}

pub fn print_all() void {
    print();
    test1.print();
    test2();
    test3();
    test4.print();
    test5();
}

pub fn print() void {
    std.log.info("main", .{});
}

test "basic test" {
    try std.testing.expectEqual(10, 3 + 7);
}
