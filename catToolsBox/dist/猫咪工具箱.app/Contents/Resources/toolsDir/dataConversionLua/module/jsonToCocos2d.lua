

-- 添加同一目录下的文件
json = require("json")

function clone(object)
    local lookup_table = {}
    local function _copy(object)
        if type(object) ~= "table" then
            return object
        elseif lookup_table[object] then
            return lookup_table[object]
        end
        local new_table = {}
        lookup_table[object] = new_table
        for key, value in pairs(object) do
            new_table[_copy(key)] = _copy(value)
        end
        return setmetatable(new_table, getmetatable(object))
    end
    return _copy(object)
end

function isnumber(v)
    return type(v) == "number"
end



-- 添加同一目录下的文件
local  AccountDataHandle = require("AccountDataHandle")





function dataConversion(name)
	
	
	local data = AccountDataHandle:uncompressAccountData(json.decode(name))
	local xmlStr = ""
	
	xmlStr = xmlStr .. "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
	xmlStr = xmlStr .."<userDefaultRoot>\n"
	xmlStr = xmlStr .. "<USTORE_TABLE_FOR_CLEAR>{\"bb_parent\":["
	
	if not data then
		return "错误"
	end
	for i, item in pairs(data) do
		xmlStr = xmlStr .. "\"" .. i .. "\","
	end
	xmlStr = xmlStr:sub(1, -2)
	xmlStr = xmlStr .. "]}</USTORE_TABLE_FOR_CLEAR>\n"
	
	for i, item in pairs(data) do
	xmlStr = xmlStr .. "<" .. i .. ">" .. data[i] .. "</" .. i .. ">\n"
	end
	xmlStr = xmlStr .. "</userDefaultRoot>"
	
	--for key in data:
	--    xmlStr += "\"" + key + "\","
	--    #最后一个不加，
	--xmlStr = xmlStr[:-1]
	--xmlStr += "]}</USTORE_TABLE_FOR_CLEAR>\n"
	--for key in data:
	--    xmlStr += "<" + key + ">" + data[key] + "</" + key + ">\n"
	--xmlStr += "</userDefaultRoot>"
	
	return xmlStr
	
	end