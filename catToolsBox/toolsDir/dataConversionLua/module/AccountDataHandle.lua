---------------------------
-- 账号数据处理
---------------------------
local M = {}
---------------------------
local valueName = {}
local valueNameMap = {}

-- 解压 key
local unValueNameMap = {}

-- 压缩变量数组
local compressNameTab = {}

-- 后续版本新加的数据
-- local addConfig = {
-- 	-- -- 版本号 变量数组
-- 	-- { version = 31, tab = {"CAT_NODE_DESERT"}}
-- }

-- 自定义的64个字符集
local chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

local function toBase64(num)
    if num == 0 then return 'A' end
    
    local result = ''
    while num > 0 do
        local mod = num % 64
        result = string.sub(chars, mod+1, mod+1) .. result
        num = math.floor(num/64)
    end
    
    return result
end

local function fromBase64(str)
	local result = 0
	for i = 1, #str do
		result = result * 64 + string.find(chars, string.sub(str, i, i)) - 1
	end
	return result
end

local config ={
	-- 变量名 , 压缩函数, 解压函数
	-- 节点数据处理
	SHOW_ROOM_DATA = {
		"compressNodeData", "uncompressNodeData",
	},
	-- 换衣间数据处理
	LockerData = {
		"compressLockerData", "uncompressLockerData",
	},
	-- 猫咪 数据处理
	SELECT_CAT_DATA = {
		"compressCatData", "uncompressCatData",
	},
	-- 头顶数据
	CAT_NODE_OVERHEAD = {
		"compressOverheadData", "uncompressOverheadData",
	},
	-- 布尔值转换
	BOOL_DATA = {
		"compressBoolData", "uncompressBoolData",
	},
}

-- 节点数据
config.CAT_NODE_SELECT = config.SHOW_ROOM_DATA
config.CAT_NODE_TOWN = config.SHOW_ROOM_DATA
config.CAT_NODE_KITCHEN = config.SHOW_ROOM_DATA
config.CAT_NODE_PARLOR = config.SHOW_ROOM_DATA
config.CAT_NODE_DESERT = config.SHOW_ROOM_DATA

-- 布尔值转换
config.ACTIVE_TROPHY_ACTIVE = config.BOOL_DATA
config.CAT_NEW_GAME_SIGN = config.BOOL_DATA
config.woodBoardShow = config.BOOL_DATA
config.NEW_ADD_ITEM = config.BOOL_DATA
config.RECORD_FIRST_UNLOCK = config.BOOL_DATA
config.MAGIC_FOOD_TABLE = config.BOOL_DATA
config.DIY_ROOM_BUY_CLICK_DATA = config.BOOL_DATA

local noSaveData = {


	-- 肯定不要
	"CAT_NODE_FOREST", "CAT_NODE_FLOWERSEA", "CAT_NODE_SKYCITY", "CAT_NODE_PARADISE",
	"CAT_FRAME_TAB", "USTORE_TABLE_FOR_CLEAR", "CAT_CHANGEKEY",
	-- 中间
	"CAT_TODAY_DATA", "RUBBISH_TIME",
	-- 看情况不要
	"CAT_HAS_PLAYBACK", "TOWN_SEESTAR_TASK", "CAT_TASK_DATA","DIY_ROOM_PHOTO_ID",
}

function M:init()
	local compressNameTabData = ST.getTable("COMPRESS_DATA_NAME_TAB")
	if not compressNameTabData then
		return
	else
		compressNameTab = {}
		for i,v in ipairs(compressNameTabData) do
			compressNameTab[v] = true
		end
	end
	local valueNameMapData = ST.getTable("valueNameMap")
	valueName = {}
	valueNameMap = {}
	for i,v in ipairs(valueNameMapData) do
		valueNameMap[v] = i
		table.insert(valueName, v)
	end
end

-- 压缩账号数据
function M:compressAccountData(data)
	local str1 = json.encode(data)
	local time = os.clock()
	print("压缩前", string.len(str1))


	local newDataTab = clone(data)

	for i, item in pairs(newDataTab) do
		if config[i] then
			local compressFunc = config[i][1]
			if self[compressFunc] then
				local newData = self[compressFunc](self, json.decode(item))
				if newData then
					newDataTab[i] = json.encode(newData)
					compressNameTab[i] = true
				else
					print("压缩失败", i)
				end
			end
		-- 开始带BB_/或者LD_BB_的数据
		elseif string.sub(i, 1, 3) == "BB_" then
			newDataTab[i] = nil
		elseif string.sub(i, 1, 5) == "LD_BB" then
			newDataTab[i] = nil
		end
	end

	local newValueNameMap = {}
	for i, item in pairs(valueNameMap) do
		newValueNameMap[item] = i
	end
	newDataTab["valueNameMap"] = json.encode(newValueNameMap)

	local compressNameTabData = {}
	for i, item in pairs(compressNameTab) do
		table.insert(compressNameTabData, i)
	end
	newDataTab["COMPRESS_DATA_NAME_TAB"] =  json.encode(compressNameTabData)

	for i,v in ipairs(noSaveData) do
		newDataTab[v] = nil
	end

	local str2 = json.encode(newDataTab)
	print("压缩后", string.len(str2))
	print("压缩比例", string.format( "%.2f", 100 - string.len(str2) / string.len(str1) * 100 ).."%")
	print("压缩时间", os.clock() - time)
	return newDataTab
end


-- 解压账号数据
function M:uncompressAccountData(data)
	if not data then
		return
	end
	-- 没有这个数值，是之前的数据不需要压缩
	if not data["valueNameMap"] then
		print("没有这个数值，是之前的数据不需要解压")
		return data
	end
	local str1 = json.encode(data)
	print("解压前", string.len(str1))
	local newDataTab = clone(data)

	unValueNameMap = json.decode(newDataTab["valueNameMap"])

	local compressNameTabData = json.decode(newDataTab["COMPRESS_DATA_NAME_TAB"])
	compressNameTab = {}
	if not compressNameTabData then
		for i, item in pairs(config) do
			compressNameTab[i] = i
		end
	else
		for i,v in ipairs(compressNameTabData) do
			compressNameTab[v] = true
		end
	end

	valueNameMap = {}
	valueName = {}
	for i,v in ipairs(unValueNameMap) do
		valueNameMap[v] = i
		table.insert(valueName, v)
	end

	for i, item in pairs(newDataTab) do
		if compressNameTab[i] and config[i] then
			local uncompressFunc = config[i][2]
			if self[uncompressFunc] then
				local newData = self[uncompressFunc](self, json.decode(item))
				if newData then
					newDataTab[i] = json.encode(newData)
					-- print(newDataTab[i] )
					-- print(string.len(newDataTab[i]))
				else
					print("解压失败", i)
				end
			end
		end
	end

	-- newDataTab["keyMap"] = nil
	-- newDataTab["valueNameMap"] = nil
	-- newDataTab["COMPRESS_DATA_NAME_TAB"] = nil
	local str2 = json.encode(newDataTab)
	print("解压后", string.len(str2))
	print("解压比例", string.format( "%.2f", string.len(str2) / string.len(str1) * 100 -100).."%")
	return newDataTab
end

---------------------------
-- 调试代码
---------------------------
-- 下载数据还原
function M:restore(data)
	local data = {}
	-- 获取全部本地数据
	local value = ifnil(json.decode(cc.UserDefault:sharedUserDefault():getStringForKey("USTORE_TABLE_FOR_CLEAR")),{})
	-- 获取数据
	for i,v in ipairs(value) do
		if string.sub(i, 1, 4) == "cat_" then
	        local value = cc.UserDefault:sharedUserDefault():getStringForKey(v)
	        if value ~= "" then
	        	data[v] = value
	        end
	    end
    end
    for k,w in pairs(value) do
        if istable(w) then
            for i,v in ipairs(w) do
                local value = cc.UserDefault:sharedUserDefault():getStringForKey(v)
		        if value ~= "" then
		        	data[v] = value
		        end
            end
        elseif isstring(w) then
            local value = cc.UserDefault:sharedUserDefault():getStringForKey(w)
	        if value ~= "" then
	        	data[w] = value
	        end
        end
    end

	-- 恢复数据
	local oldData = self:uncompressAccountData(data)
	ST.clearUStore()
	for name, value in pairs(oldData) do
		ST.setStringForKey(name, value)
	end
end

-- local dataHandle = import("com.AccountDataHandle")
-- dataHandle:debug()

-- 自调试
function M:debug()
		local data = {}
	-- 获取全部本地数据
	local value = ifnil(json.decode(cc.UserDefault:sharedUserDefault():getStringForKey("USTORE_TABLE_FOR_CLEAR")),{})
	-- 获取数据
	for i,v in ipairs(value) do
		if string.sub(i, 1, 4) == "cat_" then
			local value = cc.UserDefault:sharedUserDefault():getStringForKey(v)
			if value ~= "" then
				data[v] = value
			end
		end
	end
	for k,w in pairs(value) do
		if istable(w) then
			for i,v in ipairs(w) do
				local value = cc.UserDefault:sharedUserDefault():getStringForKey(v)
				if value ~= "" then
					data[v] = value
				end
			end
		elseif isstring(w) then
			local value = cc.UserDefault:sharedUserDefault():getStringForKey(w)
			if value ~= "" then
				data[w] = value
			end
		end
	end

	local newData = self:compressAccountData(data)
	-- 恢复数据
	local oldData = self:uncompressAccountData(newData)

	ST.clearUStore()
	for name, value in pairs(oldData) do
		ST.setStringForKey(name, value)
		ST.getKey(name)
	end
end

---------------------------
-- 统一数据处理
---------------------------
-- 布尔值转换
function M:boolNumToBool(value)
	if value == 1 then
		return true
	else
		return false
	end
end

-- 布尔值转换
-- @param value 布尔值
-- @param isNull 是否为null
function M:boolToBoolNum(value, isNull)
	if value then
		return 1
	else
		if isNull then
			return nil
		else
			return 0
		end
	end
end

-- 数字字符串下标改成数字
function M:changeNumIndex(tab)
	for i,v in pairs(tab) do
		if tonumber(i) and not isnumber(i) then
			tab[tonumber(i)] = v
			tab[i] = nil
		else
			tab[i] = v
		end
	end
	return tab
end

---------------------------
-- 节点数据处理
---------------------------

-- skinData数据处理
function M:skinDataCompress(data)
	for i,v in pairs(data) do
		v[1] = v.zor
		v[2] = tonumber(string.format("%.2f",  v.pos.x))
		v[3] = tonumber(string.format("%.2f",  v.pos.y))
		v[4] = v.name
		if v.color then
			if not v[4] then
				v[4] = 0
			end
			v[5] = v.color
		end
		v.zor = nil
		v.color = nil
		v.pos = nil
		v.name = nil

	end
	return data
end

function M:skinDataUncompress(data)
	if not data then
		return
	end
	for i,v in pairs(data) do
		self:changeNumIndex(v)
		v.zor = v[1]
		v.pos = {}
		v.pos.x = v[2]
		v.pos.y = v[3]
		v.name = v[4]
		if v.name == 0 then
			v.name = nil
		end
		if v[5] then
			v.color = v[5]
		end
		v[1] = nil
		v[2] = nil
		v[3] = nil
		v[4] = nil
		v[5] = nil
	end
	return data
end

function M:D_furnitureCompress(v)
	if v.params.skinData then
		local skinData = v.params.skinData
		skinData[1] = self:skinDataCompress(skinData.body)
		skinData[2] = self:skinDataCompress(skinData.decorate)
		skinData[3] = self:skinDataCompress(skinData.head)
		skinData[4] = self:skinDataCompress(skinData.tail)
		skinData.body = nil
		skinData.decorate = nil
		skinData.head = nil
		skinData.tail = nil
	end
end

-- 解压
function M:D_furnitureUncompress(v)
	if v.params.skinData then
		local skinData = v.params.skinData
		skinData.body = self:skinDataUncompress(skinData[1])
		skinData.decorate = self:skinDataUncompress(skinData[2])
		skinData.head = self:skinDataUncompress(skinData[3])
		skinData.tail = self:skinDataUncompress(skinData[4])
		skinData[1] = nil
		skinData[2] = nil
		skinData[3] = nil
		skinData[4] = nil
	end
end


-- 压缩节点数据
function M:compressNodeData(data)
	if not data then
		return
	end
	-- for i,v in ipairs(data) do
	for i = #data, 1, -1 do
		local v = data[i]
		if not v.time then
			-- 照片的Io路径存在清除照片数据
			if (v.node == "D_photo" and v.params.path and IO.exists(v.params.path) ) then
				table.remove(data, i)
			else
				v[1] = self:getKey(v.node)
				v[2] = tonumber(string.format("%.2f", v.params.position.x))
				v[3] = tonumber(string.format("%.2f", v.params.position.y))

				if self[v.node.."Compress"] then
					self[v.node.."Compress"](self, v)
				end
				v.params.position = nil
				v[4] = nil
				v.params.createTime = nil
				for i1,v1 in pairs(v.params) do
					if not v[4] then
						v[4] = {}
					end
					if i1 == "name"  then
						v[4][tostring(self:getKey(i1, true))] = self:getKey(v1)
					elseif i1 ~= "position"  then
						v[4][tostring(self:getKey(i1, true))] = v1
					end
				end
				v.params = nil
				if v.child then
					if #v.child == 0 then
						v[5] = nil
						v.child = nil
					else
						if not v[4] then
							v[4] = 0
						end
						v[5] = v.child
						self:compressNodeData(v.child)
						v.child = nil
					end
				else
					v[5] = nil
				end
				v.node = nil
			end
		end
	end
	return data
end

--
function M:getKey(keyName, is64Base)
	if not valueNameMap[keyName] then
		-- keyIndex = keyIndex + 1
		table.insert(valueName, keyName)
		valueNameMap[keyName] = #valueName
	end
	-- local num = valueNameMap[keyName]
	-- -- 改成16进制
	-- return string.format("%x", num)
	-- -- 改成64进制
	-- return toBase64(valueNameMap[keyName])
	if is64Base then
		return toBase64(valueNameMap[keyName])
	else
		return valueNameMap[keyName]
	end
end

--
function M:getKeyVal(index, is64Base)
	-- 改成64进制
	local num = 0
	if is64Base then
		num = fromBase64(index)
	else
		num = tonumber(index)
	end
	if not unValueNameMap[num] then
		print("没有这个数值", num)
	end
	return unValueNameMap[num]
end

function M:uncompressNodeData(data)
	--
	if not data then
		return
	end

	for i,v in ipairs(data) do
		if not v.time then
			self:changeNumIndex(v)
			v.node = self:getKeyVal(v[1])
			v.params = {}
			v.params.position = {}
			v.params.position.x = v[2]
			v.params.position.y = v[3]
			v[1] = nil
			v[2] = nil
			v[3] = nil
			if v[4] and v[4] ~= 0 then
				for i1,v1 in pairs(v[4]) do
					v.params[self:getKeyVal(i1, true)] = v1
					if self:getKeyVal(i1, true) == "name" then
						v.params.name = self:getKeyVal(v1)
					end
				end
			end
			v[4] = nil
			if self[v.node.."Uncompress"] then
				self[v.node.."Uncompress"](self, v)
			end

			if v[5] then
				v.child = v[5]
				self:uncompressNodeData(v.child)
				v[5] = nil
			end
		end

	end
	return data
end

---------------------------
-- 换衣间数据处理
---------------------------

-- 数据修改
function M:modifyLockerData(tab)
	for i,v in ipairs(tab) do
		v[1] = v.indexid
		v[2] = v.id
		v[3] = self:boolToBoolNum(v.isbuy)
		v[4] = self:boolToBoolNum(v.incat)
		v[5] = self:boolToBoolNum(v.null, true)
		v.indexid = nil
		v.id = nil
		v.isbuy = nil
		v.incat = nil
		v.null = nil
	end
end

-- 还原数据
function M:unmodifyLockerData(tab)
	for i,v in ipairs(tab) do
		self:changeNumIndex(v)
		v.indexid = v[1]
		v.id = v[2]
		v.isbuy = self:boolNumToBool(v[3])
		v.incat = self:boolNumToBool(v[4])
		v.null  = self:boolNumToBool(v[5])
		v[1] = nil
		v[2] = nil
		v[3] = nil
		v[4] = nil
		v[5] = nil
	end
end

-- 压缩换衣间数据
function M:compressLockerData(data)
	local newData = {}
	newData[1] = data.TIEIDS
	newData[2] = data.GLASSIDS
	newData[3] = data.CLOTHIDS
	newData[4] = data.HATIDS
	for i,v in ipairs(newData) do
		self:modifyLockerData(v)
	end
	return newData
end

function M:uncompressLockerData(data)
	local newData = {}
	local nameTab = {"TIEIDS", "GLASSIDS", "CLOTHIDS", "HATIDS"}
	for i,v in ipairs(data) do
		newData[nameTab[i]] = v
		self:unmodifyLockerData(v)
	end
	return newData
end

---------------------------
-- 猫咪数据处理
---------------------------
-- diyData数据处理
function M:modifyDiyData(tab)
	if not tab then
		return
	end
	-- 部件是否可以消失
	local partsTab = {
		body = 1, head = 2, limbs = 3, ear = 4, eyebrow = 5,
		rouge = 6, eye = 7, mouth = 8, tail = 9, antenna = 10,
		horn = 11, wing = 12,
	}
	for i,v in ipairs(tab) do
		v[1] = partsTab[v.parts]
		if not v[1] then
			v[1] = v.parts
		end
		v[2] = v.id
		if tonumber(v.color) and tonumber(v.color) ~= 0 then
			v[3] = tonumber(string.format("%.2f", v.color))
		end
		v.parts = nil
		v.color = nil
		v.id = nil
	end
	return tab
end

-- diyData数据还原
function M:unmodifyDiyData(tab)
	if not tab then
		return
	end
	local partsTab = {
		[1] = "body", [2] = "head", [3] = "limbs", [4] = "ear", [5] = "eyebrow",
		[6] = "rouge", [7] = "eye", [8] = "mouth", [9] = "tail", [10] = "antenna",
		[11] = "horn", [12] = "wing",
	}
	for i,v in ipairs(tab) do
		self:changeNumIndex(v)
		v.parts = partsTab[v[1]]
		if v[3] and tonumber(v[3]) ~= 0 then
			v.color = v[3]
		end
		v.id = v[2]
		v[1] = nil
		v[2] = nil
		v[3] = nil
	end
	return tab
end


-- 压缩猫咪数据
function M:compressCatData(data)
	if not data then
		return
	end
	local newData = {}
	for i,v in pairs(data) do
		newData[i] = {}
		newData[i][1] = v.index
		newData[i][2] = v.typeId
		newData[i][3] = self:boolToBoolNum(v.inBar)
		newData[i][4] = self:boolToBoolNum(v.isCanDiy)
		newData[i][5] = v.payId
		if not newData[i][5] then
			newData[i][5] = 0
		end
		newData[i][6] = v.demand
		newData[i][7] = v.change
		newData[i][8] = self:modifyDiyData(v.diyData)
		v.index = nil
		v.typeId = nil
		v.inBar = nil
		v.isCanDiy = nil
		v.payId = nil
		v.demand = nil
		v.change = nil
		v.diyData = nil
		newData[i][9] = nil
		for i1,v1 in pairs(v) do
			if v1 then
				if not newData[i][9] then
					newData[i][9] = {}
				end
				newData[i][9][i1] = v1
			end
		end
	end
	return newData
end

-- 解压猫咪数据
function M:uncompressCatData(data)
	local newData = {}
	for i,v in pairs(data) do
		self:changeNumIndex(v)
		newData[i] = {}
		newData[i].index = v[1]
		newData[i].typeId = v[2]
		newData[i].inBar = self:boolNumToBool(v[3])
		newData[i].isCanDiy = self:boolNumToBool(v[4])
		newData[i].payId = v[5]
		if newData[i].payId == 0 then
			newData[i].payId = nil
		end
		newData[i].demand = v[6]
		newData[i].change = v[7]
		newData[i].diyData = self:unmodifyDiyData(v[8])
		if v[9] then
			for i1,v1 in pairs(v[9]) do
				newData[i][i1] = v1
			end
		end
	end
	return newData
end

---------------------------
-- 头顶数据
---------------------------

-- 压缩头顶数据
function M:compressOverheadData(data)
	local newData = {}
	for i, item in ipairs(data) do
		local newItem = {}
		if item[1] and isnumber(item[1]) then
			newItem[1] = item[1]
			table.remove(item, 1)
			newItem[2] = self:compressNodeData(item)
			table.insert(newData, newItem)
		end
	end
	return newData
end

-- 解压头顶数据
function M:uncompressOverheadData(data)
	if not data then
		return
	end
	local newData = {}
	for i, item in ipairs(data) do
		local newItem = {}
		newItem = self:uncompressNodeData(item[2])
		table.insert(newItem, 1, item[1])
		table.insert(newData, newItem)
	end

	return newData
end

---------------------------
-- 布尔数据
---------------------------

-- 压缩布尔数据
function M:compressBoolData(data)
	local newData = {}
	local falg = false
	for i,v in pairs(data) do
		newData[i] = self:boolToBoolNum(v)
		if newData[i] == 0 then
			falg = true
		end
	end
	if not falg then
		newData = {}
		for i,v in pairs(data) do
			table.insert(newData, i)
		end
	end
	return newData
end

-- 解压布尔数据
function M:uncompressBoolData(data)
	local newData = {}
	for i,v in pairs(data) do
		if type(v) == "number" then
			newData[i] = self:boolNumToBool(v)
		else
			newData[v] = true
		end
	end
	return newData
end


return M