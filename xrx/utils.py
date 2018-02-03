def readlines_by(handle, line_separator=b"\n", chunk_size=64):
    buf = b""  # storage buffer
    while not handle.closed:  # while our handle is open
        data = handle.read(chunk_size)  # read `chunk_size` sized data from the passed handle
        if not data:  # no more data...
            break  # break away...
        buf += data  # add the collected data to the internal buffer
        if line_separator in buf:  # we've encountered a separator
            chunks = buf.split(line_separator)
            buf = chunks.pop()  # keep the last entry in our buffer
            for chunk in chunks:  # yield the rest
                yield chunk + line_separator
    if buf:
        yield buf  # return the last buffer if any
