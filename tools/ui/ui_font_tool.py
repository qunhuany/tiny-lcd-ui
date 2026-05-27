# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'font_tool.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPlainTextEdit, QPushButton, QScrollArea,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QSplitter, QTextEdit, QVBoxLayout, QWidget)

class Ui_FontToolWidget(object):
    def setupUi(self, FontToolWidget):
        if not FontToolWidget.objectName():
            FontToolWidget.setObjectName(u"FontToolWidget")
        FontToolWidget.resize(1040, 720)
        FontToolWidget.setMinimumSize(QSize(1040, 640))
        self.mainLayout = QVBoxLayout(FontToolWidget)
        self.mainLayout.setSpacing(8)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.configGroupBox = QGroupBox(FontToolWidget)
        self.configGroupBox.setObjectName(u"configGroupBox")
        self.configGridLayout = QGridLayout(self.configGroupBox)
        self.configGridLayout.setObjectName(u"configGridLayout")
        self.configGridLayout.setHorizontalSpacing(8)
        self.configGridLayout.setVerticalSpacing(6)
        self.fontPathLabel = QLabel(self.configGroupBox)
        self.fontPathLabel.setObjectName(u"fontPathLabel")

        self.configGridLayout.addWidget(self.fontPathLabel, 0, 0, 1, 1)

        self.fontPathValueLabel = QLabel(self.configGroupBox)
        self.fontPathValueLabel.setObjectName(u"fontPathValueLabel")
        self.fontPathValueLabel.setMinimumSize(QSize(180, 0))
        self.fontPathValueLabel.setFrameShape(QFrame.StyledPanel)

        self.configGridLayout.addWidget(self.fontPathValueLabel, 0, 1, 1, 1)

        self.browseFontButton = QPushButton(self.configGroupBox)
        self.browseFontButton.setObjectName(u"browseFontButton")

        self.configGridLayout.addWidget(self.browseFontButton, 0, 2, 1, 1)

        self.fontSizeLabel = QLabel(self.configGroupBox)
        self.fontSizeLabel.setObjectName(u"fontSizeLabel")

        self.configGridLayout.addWidget(self.fontSizeLabel, 0, 3, 1, 1)

        self.fontSizeSpinBox = QSpinBox(self.configGroupBox)
        self.fontSizeSpinBox.setObjectName(u"fontSizeSpinBox")
        self.fontSizeSpinBox.setMinimumSize(QSize(84, 0))
        self.fontSizeSpinBox.setMinimum(6)
        self.fontSizeSpinBox.setMaximum(64)
        self.fontSizeSpinBox.setValue(16)

        self.configGridLayout.addWidget(self.fontSizeSpinBox, 0, 4, 1, 1)

        self.thresholdLabel = QLabel(self.configGroupBox)
        self.thresholdLabel.setObjectName(u"thresholdLabel")

        self.configGridLayout.addWidget(self.thresholdLabel, 0, 5, 1, 1)

        self.thresholdSpinBox = QSpinBox(self.configGroupBox)
        self.thresholdSpinBox.setObjectName(u"thresholdSpinBox")
        self.thresholdSpinBox.setMinimumSize(QSize(84, 0))
        self.thresholdSpinBox.setMinimum(0)
        self.thresholdSpinBox.setMaximum(255)
        self.thresholdSpinBox.setValue(128)

        self.configGridLayout.addWidget(self.thresholdSpinBox, 0, 6, 1, 1)

        self.glyphStoreLabel = QLabel(self.configGroupBox)
        self.glyphStoreLabel.setObjectName(u"glyphStoreLabel")

        self.configGridLayout.addWidget(self.glyphStoreLabel, 1, 0, 1, 1)

        self.glyphStorePathValueLabel = QLabel(self.configGroupBox)
        self.glyphStorePathValueLabel.setObjectName(u"glyphStorePathValueLabel")
        self.glyphStorePathValueLabel.setMinimumSize(QSize(180, 0))
        self.glyphStorePathValueLabel.setFrameShape(QFrame.StyledPanel)

        self.configGridLayout.addWidget(self.glyphStorePathValueLabel, 1, 1, 1, 1)

        self.browseGlyphStoreButton = QPushButton(self.configGroupBox)
        self.browseGlyphStoreButton.setObjectName(u"browseGlyphStoreButton")

        self.configGridLayout.addWidget(self.browseGlyphStoreButton, 1, 2, 1, 1)

        self.outputDirLabel = QLabel(self.configGroupBox)
        self.outputDirLabel.setObjectName(u"outputDirLabel")

        self.configGridLayout.addWidget(self.outputDirLabel, 1, 3, 1, 1)

        self.outputDirValueLabel = QLabel(self.configGroupBox)
        self.outputDirValueLabel.setObjectName(u"outputDirValueLabel")
        self.outputDirValueLabel.setMinimumSize(QSize(180, 0))
        self.outputDirValueLabel.setFrameShape(QFrame.StyledPanel)

        self.configGridLayout.addWidget(self.outputDirValueLabel, 1, 4, 1, 2)

        self.browseOutputDirButton = QPushButton(self.configGroupBox)
        self.browseOutputDirButton.setObjectName(u"browseOutputDirButton")

        self.configGridLayout.addWidget(self.browseOutputDirButton, 1, 6, 1, 1)


        self.mainLayout.addWidget(self.configGroupBox)

        self.mainSplitter = QSplitter(FontToolWidget)
        self.mainSplitter.setObjectName(u"mainSplitter")
        self.mainSplitter.setOrientation(Qt.Horizontal)
        self.charsetGroupBox = QGroupBox(self.mainSplitter)
        self.charsetGroupBox.setObjectName(u"charsetGroupBox")
        self.charsetGroupBox.setMinimumSize(QSize(240, 0))
        self.charsetLayout = QVBoxLayout(self.charsetGroupBox)
        self.charsetLayout.setObjectName(u"charsetLayout")
        self.charsetTextEdit = QPlainTextEdit(self.charsetGroupBox)
        self.charsetTextEdit.setObjectName(u"charsetTextEdit")

        self.charsetLayout.addWidget(self.charsetTextEdit)

        self.charsetButtonLayout = QHBoxLayout()
        self.charsetButtonLayout.setObjectName(u"charsetButtonLayout")
        self.loadCharsetFileButton = QPushButton(self.charsetGroupBox)
        self.loadCharsetFileButton.setObjectName(u"loadCharsetFileButton")

        self.charsetButtonLayout.addWidget(self.loadCharsetFileButton)

        self.applyCharsetButton = QPushButton(self.charsetGroupBox)
        self.applyCharsetButton.setObjectName(u"applyCharsetButton")

        self.charsetButtonLayout.addWidget(self.applyCharsetButton)


        self.charsetLayout.addLayout(self.charsetButtonLayout)

        self.charsetSummaryLabel = QLabel(self.charsetGroupBox)
        self.charsetSummaryLabel.setObjectName(u"charsetSummaryLabel")

        self.charsetLayout.addWidget(self.charsetSummaryLabel)

        self.mainSplitter.addWidget(self.charsetGroupBox)
        self.glyphEditorScrollArea = QScrollArea(self.mainSplitter)
        self.glyphEditorScrollArea.setObjectName(u"glyphEditorScrollArea")
        self.glyphEditorScrollArea.setMinimumSize(QSize(330, 0))
        self.glyphEditorScrollArea.setWidgetResizable(True)
        self.glyphEditorScrollContents = QWidget()
        self.glyphEditorScrollContents.setObjectName(u"glyphEditorScrollContents")
        self.glyphEditorScrollContents.setGeometry(QRect(0, 0, 360, 680))
        self.glyphEditorScrollLayout = QVBoxLayout(self.glyphEditorScrollContents)
        self.glyphEditorScrollLayout.setObjectName(u"glyphEditorScrollLayout")
        self.glyphEditorGroupBox = QGroupBox(self.glyphEditorScrollContents)
        self.glyphEditorGroupBox.setObjectName(u"glyphEditorGroupBox")
        self.glyphDetailLayout = QVBoxLayout(self.glyphEditorGroupBox)
        self.glyphDetailLayout.setSpacing(8)
        self.glyphDetailLayout.setObjectName(u"glyphDetailLayout")
        self.glyphInputLayout = QHBoxLayout()
        self.glyphInputLayout.setObjectName(u"glyphInputLayout")
        self.glyphInputLabel = QLabel(self.glyphEditorGroupBox)
        self.glyphInputLabel.setObjectName(u"glyphInputLabel")

        self.glyphInputLayout.addWidget(self.glyphInputLabel)

        self.glyphInputEdit = QLineEdit(self.glyphEditorGroupBox)
        self.glyphInputEdit.setObjectName(u"glyphInputEdit")
        self.glyphInputEdit.setMinimumSize(QSize(72, 0))
        self.glyphInputEdit.setMaxLength(1)

        self.glyphInputLayout.addWidget(self.glyphInputEdit)

        self.loadGlyphButton = QPushButton(self.glyphEditorGroupBox)
        self.loadGlyphButton.setObjectName(u"loadGlyphButton")

        self.glyphInputLayout.addWidget(self.loadGlyphButton)


        self.glyphDetailLayout.addLayout(self.glyphInputLayout)

        self.glyphInfoFormLayout = QFormLayout()
        self.glyphInfoFormLayout.setObjectName(u"glyphInfoFormLayout")
        self.glyphCodepointLabel = QLabel(self.glyphEditorGroupBox)
        self.glyphCodepointLabel.setObjectName(u"glyphCodepointLabel")

        self.glyphInfoFormLayout.setWidget(0, QFormLayout.LabelRole, self.glyphCodepointLabel)

        self.glyphCodepointEdit = QLineEdit(self.glyphEditorGroupBox)
        self.glyphCodepointEdit.setObjectName(u"glyphCodepointEdit")
        self.glyphCodepointEdit.setReadOnly(True)

        self.glyphInfoFormLayout.setWidget(0, QFormLayout.FieldRole, self.glyphCodepointEdit)

        self.glyphSourceLabel = QLabel(self.glyphEditorGroupBox)
        self.glyphSourceLabel.setObjectName(u"glyphSourceLabel")

        self.glyphInfoFormLayout.setWidget(1, QFormLayout.LabelRole, self.glyphSourceLabel)

        self.glyphSourceEdit = QLineEdit(self.glyphEditorGroupBox)
        self.glyphSourceEdit.setObjectName(u"glyphSourceEdit")
        self.glyphSourceEdit.setReadOnly(True)

        self.glyphInfoFormLayout.setWidget(1, QFormLayout.FieldRole, self.glyphSourceEdit)


        self.glyphDetailLayout.addLayout(self.glyphInfoFormLayout)

        self.glyphPreviewLabel = QLabel(self.glyphEditorGroupBox)
        self.glyphPreviewLabel.setObjectName(u"glyphPreviewLabel")
        self.glyphPreviewLabel.setMinimumSize(QSize(260, 260))
        self.glyphPreviewLabel.setFrameShape(QFrame.Box)
        self.glyphPreviewLabel.setAlignment(Qt.AlignCenter)

        self.glyphDetailLayout.addWidget(self.glyphPreviewLabel)

        self.glyphShiftLayout = QGridLayout()
        self.glyphShiftLayout.setObjectName(u"glyphShiftLayout")
        self.shiftGlyphUpButton = QPushButton(self.glyphEditorGroupBox)
        self.shiftGlyphUpButton.setObjectName(u"shiftGlyphUpButton")

        self.glyphShiftLayout.addWidget(self.shiftGlyphUpButton, 0, 1, 1, 1)

        self.shiftGlyphLeftButton = QPushButton(self.glyphEditorGroupBox)
        self.shiftGlyphLeftButton.setObjectName(u"shiftGlyphLeftButton")

        self.glyphShiftLayout.addWidget(self.shiftGlyphLeftButton, 1, 0, 1, 1)

        self.clearGlyphButton = QPushButton(self.glyphEditorGroupBox)
        self.clearGlyphButton.setObjectName(u"clearGlyphButton")

        self.glyphShiftLayout.addWidget(self.clearGlyphButton, 1, 1, 1, 1)

        self.shiftGlyphRightButton = QPushButton(self.glyphEditorGroupBox)
        self.shiftGlyphRightButton.setObjectName(u"shiftGlyphRightButton")

        self.glyphShiftLayout.addWidget(self.shiftGlyphRightButton, 1, 2, 1, 1)

        self.shiftGlyphDownButton = QPushButton(self.glyphEditorGroupBox)
        self.shiftGlyphDownButton.setObjectName(u"shiftGlyphDownButton")

        self.glyphShiftLayout.addWidget(self.shiftGlyphDownButton, 2, 1, 1, 1)


        self.glyphDetailLayout.addLayout(self.glyphShiftLayout)

        self.glyphMetricFormLayout = QFormLayout()
        self.glyphMetricFormLayout.setObjectName(u"glyphMetricFormLayout")
        self.glyphWidthLabel = QLabel(self.glyphEditorGroupBox)
        self.glyphWidthLabel.setObjectName(u"glyphWidthLabel")

        self.glyphMetricFormLayout.setWidget(0, QFormLayout.LabelRole, self.glyphWidthLabel)

        self.glyphWidthSpinBox = QSpinBox(self.glyphEditorGroupBox)
        self.glyphWidthSpinBox.setObjectName(u"glyphWidthSpinBox")
        self.glyphWidthSpinBox.setMinimum(1)
        self.glyphWidthSpinBox.setMaximum(32)

        self.glyphMetricFormLayout.setWidget(0, QFormLayout.FieldRole, self.glyphWidthSpinBox)

        self.glyphHeightLabel = QLabel(self.glyphEditorGroupBox)
        self.glyphHeightLabel.setObjectName(u"glyphHeightLabel")

        self.glyphMetricFormLayout.setWidget(1, QFormLayout.LabelRole, self.glyphHeightLabel)

        self.glyphHeightSpinBox = QSpinBox(self.glyphEditorGroupBox)
        self.glyphHeightSpinBox.setObjectName(u"glyphHeightSpinBox")
        self.glyphHeightSpinBox.setMinimum(1)
        self.glyphHeightSpinBox.setMaximum(32)

        self.glyphMetricFormLayout.setWidget(1, QFormLayout.FieldRole, self.glyphHeightSpinBox)

        self.glyphAdvanceLabel = QLabel(self.glyphEditorGroupBox)
        self.glyphAdvanceLabel.setObjectName(u"glyphAdvanceLabel")

        self.glyphMetricFormLayout.setWidget(2, QFormLayout.LabelRole, self.glyphAdvanceLabel)

        self.glyphAdvanceSpinBox = QSpinBox(self.glyphEditorGroupBox)
        self.glyphAdvanceSpinBox.setObjectName(u"glyphAdvanceSpinBox")
        self.glyphAdvanceSpinBox.setMinimum(1)
        self.glyphAdvanceSpinBox.setMaximum(64)

        self.glyphMetricFormLayout.setWidget(2, QFormLayout.FieldRole, self.glyphAdvanceSpinBox)

        self.glyphXOffsetLabel = QLabel(self.glyphEditorGroupBox)
        self.glyphXOffsetLabel.setObjectName(u"glyphXOffsetLabel")

        self.glyphMetricFormLayout.setWidget(3, QFormLayout.LabelRole, self.glyphXOffsetLabel)

        self.glyphXOffsetSpinBox = QSpinBox(self.glyphEditorGroupBox)
        self.glyphXOffsetSpinBox.setObjectName(u"glyphXOffsetSpinBox")
        self.glyphXOffsetSpinBox.setMinimum(-32)
        self.glyphXOffsetSpinBox.setMaximum(32)

        self.glyphMetricFormLayout.setWidget(3, QFormLayout.FieldRole, self.glyphXOffsetSpinBox)

        self.glyphYOffsetLabel = QLabel(self.glyphEditorGroupBox)
        self.glyphYOffsetLabel.setObjectName(u"glyphYOffsetLabel")

        self.glyphMetricFormLayout.setWidget(4, QFormLayout.LabelRole, self.glyphYOffsetLabel)

        self.glyphYOffsetSpinBox = QSpinBox(self.glyphEditorGroupBox)
        self.glyphYOffsetSpinBox.setObjectName(u"glyphYOffsetSpinBox")
        self.glyphYOffsetSpinBox.setMinimum(-32)
        self.glyphYOffsetSpinBox.setMaximum(32)

        self.glyphMetricFormLayout.setWidget(4, QFormLayout.FieldRole, self.glyphYOffsetSpinBox)


        self.glyphDetailLayout.addLayout(self.glyphMetricFormLayout)

        self.glyphRowsEdit = QPlainTextEdit(self.glyphEditorGroupBox)
        self.glyphRowsEdit.setObjectName(u"glyphRowsEdit")
        self.glyphRowsEdit.setMaximumSize(QSize(16777215, 70))

        self.glyphDetailLayout.addWidget(self.glyphRowsEdit)

        self.glyphButtonLayout = QHBoxLayout()
        self.glyphButtonLayout.setObjectName(u"glyphButtonLayout")
        self.regenerateGlyphButton = QPushButton(self.glyphEditorGroupBox)
        self.regenerateGlyphButton.setObjectName(u"regenerateGlyphButton")

        self.glyphButtonLayout.addWidget(self.regenerateGlyphButton)

        self.applyGlyphMetricButton = QPushButton(self.glyphEditorGroupBox)
        self.applyGlyphMetricButton.setObjectName(u"applyGlyphMetricButton")

        self.glyphButtonLayout.addWidget(self.applyGlyphMetricButton)

        self.saveGlyphButton = QPushButton(self.glyphEditorGroupBox)
        self.saveGlyphButton.setObjectName(u"saveGlyphButton")

        self.glyphButtonLayout.addWidget(self.saveGlyphButton)

        self.resetGlyphButton = QPushButton(self.glyphEditorGroupBox)
        self.resetGlyphButton.setObjectName(u"resetGlyphButton")

        self.glyphButtonLayout.addWidget(self.resetGlyphButton)


        self.glyphDetailLayout.addLayout(self.glyphButtonLayout)


        self.glyphEditorScrollLayout.addWidget(self.glyphEditorGroupBox)

        self.glyphEditorScrollArea.setWidget(self.glyphEditorScrollContents)
        self.mainSplitter.addWidget(self.glyphEditorScrollArea)
        self.previewGroupBox = QGroupBox(self.mainSplitter)
        self.previewGroupBox.setObjectName(u"previewGroupBox")
        self.previewGroupBox.setMinimumSize(QSize(380, 0))
        self.previewLayout = QVBoxLayout(self.previewGroupBox)
        self.previewLayout.setObjectName(u"previewLayout")
        self.previewTextEdit = QPlainTextEdit(self.previewGroupBox)
        self.previewTextEdit.setObjectName(u"previewTextEdit")
        self.previewTextEdit.setMaximumSize(QSize(16777215, 90))

        self.previewLayout.addWidget(self.previewTextEdit)

        self.lcdPreviewLabel = QLabel(self.previewGroupBox)
        self.lcdPreviewLabel.setObjectName(u"lcdPreviewLabel")
        self.lcdPreviewLabel.setMinimumSize(QSize(384, 192))
        self.lcdPreviewLabel.setFrameShape(QFrame.Box)
        self.lcdPreviewLabel.setAlignment(Qt.AlignCenter)
        self.lcdPreviewLabel.setScaledContents(True)

        self.previewLayout.addWidget(self.lcdPreviewLabel)

        self.previewConfigLayout = QGridLayout()
        self.previewConfigLayout.setObjectName(u"previewConfigLayout")
        self.lcdWidthLabel = QLabel(self.previewGroupBox)
        self.lcdWidthLabel.setObjectName(u"lcdWidthLabel")

        self.previewConfigLayout.addWidget(self.lcdWidthLabel, 0, 0, 1, 1)

        self.lcdWidthSpinBox = QSpinBox(self.previewGroupBox)
        self.lcdWidthSpinBox.setObjectName(u"lcdWidthSpinBox")
        self.lcdWidthSpinBox.setMinimumSize(QSize(84, 0))
        self.lcdWidthSpinBox.setMinimum(1)
        self.lcdWidthSpinBox.setMaximum(512)
        self.lcdWidthSpinBox.setValue(128)

        self.previewConfigLayout.addWidget(self.lcdWidthSpinBox, 0, 1, 1, 1)

        self.lcdHeightLabel = QLabel(self.previewGroupBox)
        self.lcdHeightLabel.setObjectName(u"lcdHeightLabel")

        self.previewConfigLayout.addWidget(self.lcdHeightLabel, 0, 2, 1, 1)

        self.lcdHeightSpinBox = QSpinBox(self.previewGroupBox)
        self.lcdHeightSpinBox.setObjectName(u"lcdHeightSpinBox")
        self.lcdHeightSpinBox.setMinimumSize(QSize(84, 0))
        self.lcdHeightSpinBox.setMinimum(1)
        self.lcdHeightSpinBox.setMaximum(512)
        self.lcdHeightSpinBox.setValue(64)

        self.previewConfigLayout.addWidget(self.lcdHeightSpinBox, 0, 3, 1, 1)

        self.zoomLabel = QLabel(self.previewGroupBox)
        self.zoomLabel.setObjectName(u"zoomLabel")

        self.previewConfigLayout.addWidget(self.zoomLabel, 1, 0, 1, 1)

        self.zoomSlider = QSlider(self.previewGroupBox)
        self.zoomSlider.setObjectName(u"zoomSlider")
        self.zoomSlider.setMinimum(10)
        self.zoomSlider.setMaximum(80)
        self.zoomSlider.setSingleStep(1)
        self.zoomSlider.setPageStep(10)
        self.zoomSlider.setValue(30)
        self.zoomSlider.setOrientation(Qt.Horizontal)

        self.previewConfigLayout.addWidget(self.zoomSlider, 1, 1, 1, 3)


        self.previewLayout.addLayout(self.previewConfigLayout)

        self.previewOptionLayout = QHBoxLayout()
        self.previewOptionLayout.setObjectName(u"previewOptionLayout")
        self.showGridCheckBox = QCheckBox(self.previewGroupBox)
        self.showGridCheckBox.setObjectName(u"showGridCheckBox")

        self.previewOptionLayout.addWidget(self.showGridCheckBox)

        self.showPageGridCheckBox = QCheckBox(self.previewGroupBox)
        self.showPageGridCheckBox.setObjectName(u"showPageGridCheckBox")

        self.previewOptionLayout.addWidget(self.showPageGridCheckBox)

        self.previewOptionSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.previewOptionLayout.addItem(self.previewOptionSpacer)


        self.previewLayout.addLayout(self.previewOptionLayout)

        self.mainSplitter.addWidget(self.previewGroupBox)

        self.mainLayout.addWidget(self.mainSplitter)

        self.actionGroupBox = QGroupBox(FontToolWidget)
        self.actionGroupBox.setObjectName(u"actionGroupBox")
        self.actionRootLayout = QVBoxLayout(self.actionGroupBox)
        self.actionRootLayout.setObjectName(u"actionRootLayout")
        self.actionButtonLayout = QHBoxLayout()
        self.actionButtonLayout.setObjectName(u"actionButtonLayout")
        self.loadProjectButton = QPushButton(self.actionGroupBox)
        self.loadProjectButton.setObjectName(u"loadProjectButton")

        self.actionButtonLayout.addWidget(self.loadProjectButton)

        self.generateMissingGlyphsButton = QPushButton(self.actionGroupBox)
        self.generateMissingGlyphsButton.setObjectName(u"generateMissingGlyphsButton")

        self.actionButtonLayout.addWidget(self.generateMissingGlyphsButton)

        self.validateAllButton = QPushButton(self.actionGroupBox)
        self.validateAllButton.setObjectName(u"validateAllButton")

        self.actionButtonLayout.addWidget(self.validateAllButton)

        self.exportFirmwareFontButton = QPushButton(self.actionGroupBox)
        self.exportFirmwareFontButton.setObjectName(u"exportFirmwareFontButton")

        self.actionButtonLayout.addWidget(self.exportFirmwareFontButton)


        self.actionRootLayout.addLayout(self.actionButtonLayout)

        self.logTextEdit = QTextEdit(self.actionGroupBox)
        self.logTextEdit.setObjectName(u"logTextEdit")
        self.logTextEdit.setMaximumSize(QSize(16777215, 110))
        self.logTextEdit.setReadOnly(True)

        self.actionRootLayout.addWidget(self.logTextEdit)


        self.mainLayout.addWidget(self.actionGroupBox)


        self.retranslateUi(FontToolWidget)

        QMetaObject.connectSlotsByName(FontToolWidget)
    # setupUi

    def retranslateUi(self, FontToolWidget):
        FontToolWidget.setWindowTitle(QCoreApplication.translate("FontToolWidget", u"LCD Font Tool", None))
        self.configGroupBox.setTitle(QCoreApplication.translate("FontToolWidget", u"Input / Output", None))
        self.fontPathLabel.setText(QCoreApplication.translate("FontToolWidget", u"Font", None))
        self.fontPathValueLabel.setText(QCoreApplication.translate("FontToolWidget", u"No font selected", None))
        self.browseFontButton.setText(QCoreApplication.translate("FontToolWidget", u"Browse", None))
        self.fontSizeLabel.setText(QCoreApplication.translate("FontToolWidget", u"Size", None))
        self.thresholdLabel.setText(QCoreApplication.translate("FontToolWidget", u"Threshold", None))
        self.glyphStoreLabel.setText(QCoreApplication.translate("FontToolWidget", u"Glyphs", None))
        self.glyphStorePathValueLabel.setText(QCoreApplication.translate("FontToolWidget", u"No glyphs selected", None))
        self.browseGlyphStoreButton.setText(QCoreApplication.translate("FontToolWidget", u"Browse", None))
        self.outputDirLabel.setText(QCoreApplication.translate("FontToolWidget", u"Output", None))
        self.outputDirValueLabel.setText(QCoreApplication.translate("FontToolWidget", u"No output selected", None))
        self.browseOutputDirButton.setText(QCoreApplication.translate("FontToolWidget", u"Browse", None))
        self.charsetGroupBox.setTitle(QCoreApplication.translate("FontToolWidget", u"Charset", None))
        self.charsetTextEdit.setPlaceholderText(QCoreApplication.translate("FontToolWidget", u"Paste required characters here", None))
        self.loadCharsetFileButton.setText(QCoreApplication.translate("FontToolWidget", u"Load Text", None))
        self.applyCharsetButton.setText(QCoreApplication.translate("FontToolWidget", u"Apply", None))
        self.charsetSummaryLabel.setText(QCoreApplication.translate("FontToolWidget", u"0 chars", None))
        self.glyphEditorGroupBox.setTitle(QCoreApplication.translate("FontToolWidget", u"Glyph Editor", None))
        self.glyphInputLabel.setText(QCoreApplication.translate("FontToolWidget", u"Char", None))
        self.glyphInputEdit.setPlaceholderText(QCoreApplication.translate("FontToolWidget", u"\u8f93\u5165\u4e00\u4e2a\u5b57", None))
        self.loadGlyphButton.setText(QCoreApplication.translate("FontToolWidget", u"Load", None))
        self.glyphCodepointLabel.setText(QCoreApplication.translate("FontToolWidget", u"Codepoint", None))
        self.glyphSourceLabel.setText(QCoreApplication.translate("FontToolWidget", u"Source", None))
        self.glyphPreviewLabel.setText(QCoreApplication.translate("FontToolWidget", u"Glyph grid", None))
        self.shiftGlyphUpButton.setText(QCoreApplication.translate("FontToolWidget", u"Up", None))
        self.shiftGlyphLeftButton.setText(QCoreApplication.translate("FontToolWidget", u"Left", None))
        self.clearGlyphButton.setText(QCoreApplication.translate("FontToolWidget", u"Clear", None))
        self.shiftGlyphRightButton.setText(QCoreApplication.translate("FontToolWidget", u"Right", None))
        self.shiftGlyphDownButton.setText(QCoreApplication.translate("FontToolWidget", u"Down", None))
        self.glyphWidthLabel.setText(QCoreApplication.translate("FontToolWidget", u"Width", None))
        self.glyphHeightLabel.setText(QCoreApplication.translate("FontToolWidget", u"Height", None))
        self.glyphAdvanceLabel.setText(QCoreApplication.translate("FontToolWidget", u"Advance", None))
        self.glyphXOffsetLabel.setText(QCoreApplication.translate("FontToolWidget", u"X Offset", None))
        self.glyphYOffsetLabel.setText(QCoreApplication.translate("FontToolWidget", u"Y Offset", None))
        self.glyphRowsEdit.setPlaceholderText(QCoreApplication.translate("FontToolWidget", u"Glyph rows", None))
        self.regenerateGlyphButton.setText(QCoreApplication.translate("FontToolWidget", u"Regenerate", None))
        self.applyGlyphMetricButton.setText(QCoreApplication.translate("FontToolWidget", u"Apply", None))
        self.saveGlyphButton.setText(QCoreApplication.translate("FontToolWidget", u"Save", None))
        self.resetGlyphButton.setText(QCoreApplication.translate("FontToolWidget", u"Reset", None))
        self.previewGroupBox.setTitle(QCoreApplication.translate("FontToolWidget", u"String Preview", None))
        self.previewTextEdit.setPlaceholderText(QCoreApplication.translate("FontToolWidget", u"Type preview strings here", None))
        self.lcdPreviewLabel.setText(QCoreApplication.translate("FontToolWidget", u"String preview", None))
        self.lcdWidthLabel.setText(QCoreApplication.translate("FontToolWidget", u"Width", None))
        self.lcdHeightLabel.setText(QCoreApplication.translate("FontToolWidget", u"Height", None))
        self.zoomLabel.setText(QCoreApplication.translate("FontToolWidget", u"Zoom", None))
        self.showGridCheckBox.setText(QCoreApplication.translate("FontToolWidget", u"Grid", None))
        self.showPageGridCheckBox.setText(QCoreApplication.translate("FontToolWidget", u"Page Grid", None))
        self.actionGroupBox.setTitle(QCoreApplication.translate("FontToolWidget", u"Actions", None))
        self.loadProjectButton.setText(QCoreApplication.translate("FontToolWidget", u"Load Glyphs", None))
        self.generateMissingGlyphsButton.setText(QCoreApplication.translate("FontToolWidget", u"Generate Missing", None))
        self.validateAllButton.setText(QCoreApplication.translate("FontToolWidget", u"Validate", None))
        self.exportFirmwareFontButton.setText(QCoreApplication.translate("FontToolWidget", u"Export Firmware Font", None))
        self.logTextEdit.setPlaceholderText(QCoreApplication.translate("FontToolWidget", u"Log", None))
    # retranslateUi

