local combatIndicatorFrame = CreateFrame("Frame", "CombatIndicator", UIParent)
combatIndicatorFrame:SetSize(10, 10)
combatIndicatorFrame:SetPoint("TOPLEFT", UIParent, "TOPLEFT", 0, 0)
local tex = combatIndicatorFrame:CreateTexture(nil, "BACKGROUND")
tex:SetAllPoints(combatIndicatorFrame)

local function CombatIndicatorUpdate(self, elapsed)
    local isChanneling = UnitChannelInfo("player")
    
    if isChanneling then
        tex:SetColorTexture(0, 1, 0, 1)
    elseif InCombatLockdown() then
        if IsMounted() then
            tex:SetColorTexture(0, 1, 0, 1)
        else 
            if UnitExists("target") and not UnitIsFriend("player", "target") then
                tex:SetColorTexture(1, 0, 0, 1)
            else
                tex:SetColorTexture(0, 1, 0, 1)
            end
        end
    else
        tex:SetColorTexture(0, 1, 0, 1)
    end
    combatIndicatorFrame:Show()
end

combatIndicatorFrame:SetScript("OnUpdate", CombatIndicatorUpdate)
