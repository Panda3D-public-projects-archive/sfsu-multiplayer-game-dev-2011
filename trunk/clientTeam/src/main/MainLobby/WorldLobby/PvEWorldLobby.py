
from common.Constants import Constants
from common.DirectBasicButton import DirectBasicButton
from common.DirectWindow import DirectWindow
from direct.gui.DirectGui import DGG
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectOptionMenu import DirectOptionMenu
from main.MainLobby.WorldLobby.WorldLobbyChat import WorldLobbyChat
from panda3d.core import TextNode, TransparencyAttrib
from direct.gui.OnscreenText import OnscreenText

class PvEWorldLobby:
    
    def __init__(self):
        
                
        self.chatButtons = []
        self.chatLines = []
        self.avatarTypes=['Choose Avatar', 'Planter', 'Breeder', 'Weather Man']
        self.maxItemsVisible=23
        self.avatar=None
        self.avatarChosen = False
#        self.createBackground()
        self.createMainFrame()
        self.worldChat = WorldLobbyChat(self.mainFrame, 1)
        self.createMainFrameButtons()
        self.createMainFrameLabel()
        self.createPlayerMaps()
        self.createAvatarType()
        self.retrieveInfoFromMsgQ()
        main.msgQ.addToPendingObj(Constants.WORLD_TYPE, 0)
        self.putToCommandList()
        
    def putToCommandList(self):
        
        main.msgQ.addToCommandList(Constants.CMSG_CHOOSE_AVATAR_TYPE, self.updateAvatarType)
        main.msgQ.addToCommandList(Constants.CMSG_CANCEL_TO_JOIN_GAME, self.updateCancelGame)
        main.msgQ.addToCommandList(Constants.CMSG_JOIN_PVE_WORLD, self.responseToJoinGame)
        
    def createBackground(self):
        base.setBackgroundColor( 1.0, 1.0, 1.0 )
        
    def createMainFrame(self):
        
        self.mainFrame = DirectWindow(frameSize=(0,0,0,0),
                                     frameColor = (0,0,0,0),
                                      pos=(0,0,0))
    
    def createMainFrameButtons(self):
        
        self.backButton = DirectBasicButton(text = 'Back',
                                            text_fg = Constants.TEXT_COLOR,
                                            text_font = Constants.FONT_TYPE_02,
                                            text_pos = ( 0, -0.018),
                                            text_scale = 0.08,
                                            text_shadow = Constants.TEXT_SHADOW_COLOR,
                                            frameSize = ( -0.2, 0.2, -0.06, 0.06),
                                            frameColor = (0.8, 0.2, 0, 0.7),
                                            pos = (-1.35, 0, 0.9),
                                            relief = DGG.FLAT,
                                            command=self.requestToCancel)
        self.backButton.reparentTo(self.mainFrame)
        
        self.joinButton = DirectBasicButton(text = 'Join',
                                            text_fg = Constants.TEXT_COLOR,
                                            text_font = Constants.FONT_TYPE_02,
                                            text_pos = ( 0, -0.015),
                                            text_scale = 0.08,
                                            text_shadow = Constants.TEXT_SHADOW_COLOR,
                                            frameSize = ( -0.25, 0.25, -0.06, 0.06),
                                            frameColor = (0.8, 0.2, 0, 0.7),
                                            pos = (-0.5, 0, -0.8),
                                            relief = DGG.FLAT,
                                            command=self.requestToJoinGame)
        self.joinButton.reparentTo(self.mainFrame)
    
    def createMainFrameLabel(self):
        
        self.gameNameLable = DirectLabel(text = "Game Name",
                                         text_fg = (0,0,0,1),
                                         text_font = Constants.FONT_TYPE_01,
                                         text_pos = (0, -0.015),
                                         text_scale = 0.1,
                                         text_shadow = (0.1, 0.1, 0.1,0.7),
                                         frameColor = (0,0,0,0),
                                         pos=(-1.2, 0, 0.75))
        self.gameNameLable.reparentTo(self.mainFrame)
        
        self.ecosystemNameLabel = DirectLabel(text = "( ecosys name )",
                                         text_fg = (0,0,0,1),
                                         text_font = Constants.FONT_TYPE_01,
                                         text_pos = (0, -0.015),
                                         text_scale = 0.07,
                                         text_shadow = (0.1, 0.1, 0.1,0.7),
                                         frameColor = (0,0,0,0),
                                         pos=(-1.2, 0, 0.67))
        self.ecosystemNameLabel.reparentTo(self.mainFrame)
        
        self.timerLabel = DirectLabel(text = "4 player currently active",
                                      text_fg = (0,0,0,1),
                                      text_font = Constants.FONT_TYPE_01,
                                      text_pos = (0, -0.015),
                                      text_scale = 0.05,
                                      text_shadow = (0.1, 0.1, 0.1,0.7),
                                      frameColor = (0,0,0,0),
                                      pos=(-1.05, 0, -0.8))
        self.timerLabel.reparentTo(self.mainFrame)
        
        self.avatarItem = OnscreenText(text = 'Choose Avatar', pos = (-1.2, 0.56), scale = 0.07)
        
    def createPlayerMaps(self):
        self.playerMap = DirectLabel(image = "models/maps/minimap.png",
                                     image_scale=(0.2, 0.2,0.2),
                                     image_hpr = (0 ,-70, 30),
                                     frameSize = (-0.3, 0.3, 0.03, 0.03),
                                     frameColor = (0,0,0,1),
                                     pos=(-1.05, 0, 0))
#                                     hpr=(-70, -45, 10))
        self.playerMap.reparentTo(self.mainFrame)
    
    def createAvatarType(self):
        
        self.avatarTypeLabel = DirectLabel(text = "Avatar Type",
                                           text_fg = (1,1,1,1),
                                           text_font = Constants.FONT_TYPE_02,
                                           text_pos = ( 0, -0.015),
                                           text_scale = 0.09,
                                           frameSize = ( -0.25, 0.25, -0.06, 0.06),
                                           frameColor = (0,0,0,0),
                                           pos = (-1.15, 0, -0.65),
                                           relief = DGG.FLAT)
        self.avatarTypeLabel.reparentTo(self.mainFrame)
        
        self.avatarChoice = DirectOptionMenu(text = "Avatar Type",
                                             text_pos = (-1.6, -0.22),
                                             text_scale = 0.55,
                                             scale = 0.1,
                                             items=self.avatarTypes,
                                             initialitem = 0,
                                             frameSize = (-2.0, 2.0, -0.65, 0.65), 
                                             highlightColor = (0.9, 0.2, 0.1, 0.8),
                                             pos = (-0.6, 0 , -0.63),
                                             popupMarker_scale=0.3,
                                             command=self.requestChangeAvatar)
        self.avatarChoice.reparentTo(self.mainFrame)
        
    def retrieveInfoFromMsgQ(self):
        
        self.worldInfo = main.msgQ.getObjFromPendingObj(Constants.PENDING_WORLD_LOBBY_OBJ)
        if self.worldInfo != None:
            self.gameNameLable['text'] = self.worldInfo.worldName
            self.ecosystemNameLabel['text']=self.worldInfo.ecosystem
    
    def requestChangeAvatar(self, avatar):
        self.avatar = avatar
        if avatar != self.avatarTypes[0]:
            obj = {"worldName": self.worldInfo.worldName, "avatarType" : avatar}
            main.cManager.sendRequest(Constants.CMSG_CHOOSE_AVATAR_TYPE, obj)
    
    def updateAvatarType(self, status):
        
        print 'pve world lobby'+str(status)
        self.avatarChosen = True
        if status == 0:
            print 'update avatar type '+self.avatar
            self.avatarItem.setText(self.avatar)
        
    def requestToCancel(self):
        
        obj = {"worldName":self.worldInfo.worldName}
        main.cManager.sendRequest(Constants.CMSG_CANCEL_TO_JOIN_GAME, obj)
        main.switchEnvironment("LobbyHeader")
    
    def updateCancelGame(self, obj=None):
        
        print 'Cancel PvE'
        
    def requestToJoinGame(self):
        
        if self.avatarChosen:
            obj = {"worldName": self.worldInfo.worldName}
            main.msgQ.addToPendingObj(Constants.WORLD_TYPE, 0)
            main.msgQ.addToPendingObj(Constants.WORLD_NAME, self.worldInfo.worldName)
            main.cManager.sendRequest(Constants.CMSG_JOIN_PVE_WORLD, obj)
        
    def responseToJoinGame(self, status):
        
        if status == 0:
            main.switchEnvironment("WorldGUI") 
        else:
            print 'Fail to join'

        
    def switchToWorld(self):
        main.switchEnvironment("WorldGUI") 
        
    def unload(self):
        print 'Unload PvEWorldLobby'
        # mainFrame is the parent to all directGuiWidget, so destroy mainFrame
        # will destroy everything
        self.avatarItem.destroy()
        self.mainFrame.destroy()