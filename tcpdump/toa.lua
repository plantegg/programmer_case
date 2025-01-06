local toa_protocol = Proto("toa","Parse TOA Protocol")
local tcp_opts = Field.new("tcp.options")

local toa_type = ProtoField.uint16("toa.type", "toa type")
local toa_client_ip = ProtoField.ipv4("toa.client_ip", "Client IP Address")
local toa_client_port = ProtoField.uint16("toa.cport", "Client port")
local toa_vip = ProtoField.ipv4("toa.vip", "LVS Address")
local toa_vport = ProtoField.uint16("toa.vport", "LVS port")
local toa_client_ipv6 = ProtoField.ipv6("toa.client_ipv6", "Client IPv6 Address")
local toa_vipv6 = ProtoField.ipv6("toa.vipv6", "VIPv6 Address")

toa_protocol.fields = { 
    toa_type,
    toa_client_ip, 
    toa_client_port, 
    toa_vip,  
    toa_vport, 
    toa_client_ipv6, 
    toa_vipv6 
}

--- 以下几个 parse 函数针对不同的 toa 类型(252/254/250/249)进行解析
--- toa 252 TCPOLEN_VTOA 20  |opcode|size|cport+cip+vid+vip+vport+pad[2]|=1+1+ 2+4+4+4+2 +2 
function parse_252(v, subtree)
    local cport = v:range(0,2):uint()
    local client_ip = v:range(2, 4):ipv4()
    local vaddr_ip= v:range(10,4):ipv4()
    local vport = v:range(14,2):uint()
    print("debug/252 client:", cport, client_ip, vaddr_ip, vport)

    subtree:add(toa_client_ip, client_ip) 
    subtree:add(toa_client_port, cport)
    subtree:add(toa_vip, vaddr_ip) 
    subtree:add(toa_vport, vport)
end  

--- fe08cf882f5e575a  fe-254 08-length 8 cf88-cport
--- toa 254 TCPOLEN_VTOA 8  |opcode|size|cport+cip=1+1+ 2+4
function parse_254(v, subtree)
    local cport = v:range(0, 2):uint()
    local client_ip = v:range(2, 4):ipv4()
    print("debug/254 client:", cport, client_ip)
    subtree:add(toa_client_ip, client_ip)
    subtree:add(toa_client_port, cport)
end

--- toa 253 for smartnat TCPOLEN_VTOA 8  |opcode|size|cport+cip=1+1+ 2+4
function parse_253(v, subtree)
    local cport = v:range(0, 2):uint()
    local client_ip = v:range(2, 4):ipv4()
    print("debug/253 client:", cport, client_ip)
    subtree:add(toa_client_ip, client_ip)
    subtree:add(toa_client_port, cport)
end

function parse_250(v, subtree)
    local vport = v:range(0, 2):uint()
    local vip = v:range(2, 4):ipv4()
    print("debug/250 client:", vport, vip)
    subtree:add(toa_vip, vip)
    subtree:add(toa_vport, vport)
end 

function parse_249(v, subtree)
    local vip = v:range(0, 16):ipv6()
    print("debug/249 vip ipv6:", vip)

    local client_ip = v:range(16, 16):ipv6()
    print("debug/249 client ipv6:", client_ip)

    subtree:add(toa_vipv6, vip)
    subtree:add(toa_client_ipv6, client_ip)       
end    

function toa_protocol.dissector(buffer, pinfo, tree)
    local opts = tcp_opts()
    if (opts) then
        local len = opts.len
        local off = 0
        while (off < len)
        do
            local subtree = nil
            local kind = opts.range(off, 1):uint()
            if (kind == 1 or kind == 0) then
                off = off + 1
            else
                local toa_len = opts.range(off + 1, 1):uint()
                if (toa_len ~= 2) then
                    local v = opts.range(off + 2, toa_len - 2):tvb()

                    print("toa info:", kind, toa_len, v)
                    if (subtree == nil and kind>248 and kind<255 ) then
                        subtree = tree:add(toa_protocol, string.format("TOA Protocol: %d", kind))
                        -- 单独再次添加 toa_type 是希望可以在过滤器中搜索匹配，但不展示
                        local toa_type_item = subtree:add(toa_type, kind)
                        -- 只隐藏 toa_type,因为已经在 head 部分显示了，不再单独展示
                        toa_type_item:set_hidden(true)
                        -- 这行隐藏单独的整个 subtree，但仍然可以在过滤器中搜索匹配
                        --subtree:set_hidden(true)  
                    end
                    if (kind == 254 and toa_len == 8) then
                        parse_254(v, subtree)
                    end
                    if (kind == 253 and toa_len == 8) then
                        parse_253(v, subtree)
                    end
                    if (kind == 252 and toa_len == 20) then
                        parse_252(v, subtree)
                    end
                    if (kind == 250 and toa_len == 8) then
                        parse_250(v, subtree)
                    end
                    if (kind == 249 and toa_len >= 40) then
                        parse_249(v, subtree)
                    end
                end
                off = off + toa_len
            end
        end
    end
end

register_postdissector(toa_protocol)