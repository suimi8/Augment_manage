#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
团队管理工具 - 主应用程序
支持邀请成员、删除成员、查看团队数据等功能
"""

import sys
import json
import os
import re
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QProgressBar, QGroupBox,
    QFormLayout, QSpinBox, QCheckBox, QComboBox, QSplitter, QFrame,
    QScrollArea, QGridLayout, QStatusBar, QMenuBar, QMenu, QFileDialog,
    QGraphicsDropShadowEffect, QSizePolicy, QSystemTrayIcon
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap, QAction, QPalette, QColor


class StyleManager:
    """Modern design system - Version 5.0"""

    # New color palette - clean and professional
    PRIMARY_COLOR = "#4361ee"  # Primary blue
    PRIMARY_LIGHT = "#7b9cff"
    PRIMARY_DARK = "#2c3ebb"
    
    SECONDARY_COLOR = "#3f37c9"  # Secondary violet
    SECONDARY_LIGHT = "#7a71ff"
    SECONDARY_DARK = "#312ba8"
    
    SUCCESS_COLOR = "#22c55e"  # Success green
    SUCCESS_LIGHT = "#4ade80"
    SUCCESS_DARK = "#16a34a"
    
    DANGER_COLOR = "#ef4444"   # Error red
    DANGER_LIGHT = "#f87171"
    DANGER_DARK = "#dc2626"
    
    WARNING_COLOR = "#f97316"  # Warning orange
    WARNING_LIGHT = "#fb923c"
    WARNING_DARK = "#ea580c"
    
    INFO_COLOR = "#06b6d4"     # Info teal
    INFO_LIGHT = "#22d3ee"
    INFO_DARK = "#0891b2"
    
    NEUTRAL_LIGHT = "#f8fafc"  # Light neutral
    NEUTRAL_MEDIUM = "#e2e8f0"  # Medium neutral
    NEUTRAL_DARK = "#1e293b"   # Dark neutral
    
    BACKGROUND_COLOR = "#ffffff"  # Background
    TEXT_COLOR = "#0f172a"     # Text color
    
    SHADOW_COLOR = "rgba(0, 0, 0, 0.08)"  # Shadow

    @staticmethod
    def get_app_style():
        """Get the application style with the new design"""
        return f"""
        /* Main Window */
        QMainWindow {{
            background: #f1f5f9;
            color: {StyleManager.TEXT_COLOR};
            font-family: 'Segoe UI', 'Arial', sans-serif;
        }}

        /* Widget Styles */
        QWidget {{
            font-size: 13px;
        }}

        /* TabWidget Styles */
        QTabWidget::pane {{
            border: 1px solid {StyleManager.NEUTRAL_MEDIUM};
            background: {StyleManager.BACKGROUND_COLOR};
            border-radius: 8px;
            margin-top: -1px;
        }}

        QTabBar::tab {{
            background: {StyleManager.NEUTRAL_LIGHT};
            border: 1px solid {StyleManager.NEUTRAL_MEDIUM};
            border-bottom: none;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            padding: 10px 20px;
            margin-right: 2px;
            font-weight: 600;
            color: {StyleManager.NEUTRAL_DARK};
        }}

        QTabBar::tab:selected {{
            background: {StyleManager.BACKGROUND_COLOR};
            color: {StyleManager.PRIMARY_COLOR};
            border-bottom: 2px solid {StyleManager.PRIMARY_COLOR};
        }}

        QTabBar::tab:hover:!selected {{
            background: {StyleManager.NEUTRAL_MEDIUM}80;
        }}

        /* Button Styles */
        QPushButton {{
            background: {StyleManager.NEUTRAL_LIGHT};
            border: 1px solid {StyleManager.NEUTRAL_MEDIUM};
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
            color: {StyleManager.TEXT_COLOR};
            min-height: 20px;
        }}

        QPushButton:hover {{
            background: {StyleManager.NEUTRAL_MEDIUM};
            border: 1px solid {StyleManager.NEUTRAL_MEDIUM};
        }}

        QPushButton:pressed {{
            background: {StyleManager.NEUTRAL_MEDIUM};
        }}

        QPushButton:disabled {{
            background: {StyleManager.NEUTRAL_LIGHT};
            color: {StyleManager.NEUTRAL_MEDIUM};
            border: 1px solid {StyleManager.NEUTRAL_MEDIUM}80;
        }}

        /* Primary Button */
        QPushButton[class="primary"] {{
            background: {StyleManager.PRIMARY_COLOR};
            border: 1px solid {StyleManager.PRIMARY_DARK};
            color: white;
        }}

        QPushButton[class="primary"]:hover {{
            background: {StyleManager.PRIMARY_DARK};
        }}

        /* Success Button */
        QPushButton[class="success"] {{
            background: {StyleManager.SUCCESS_COLOR};
            border: 1px solid {StyleManager.SUCCESS_DARK};
            color: white;
        }}

        QPushButton[class="success"]:hover {{
            background: {StyleManager.SUCCESS_DARK};
        }}

        /* Danger Button */
        QPushButton[class="danger"] {{
            background: {StyleManager.DANGER_COLOR};
            border: 1px solid {StyleManager.DANGER_DARK};
            color: white;
        }}

        QPushButton[class="danger"]:hover {{
            background: {StyleManager.DANGER_DARK};
        }}

        /* Warning Button */
        QPushButton[class="warning"] {{
            background: {StyleManager.WARNING_COLOR};
            border: 1px solid {StyleManager.WARNING_DARK};
            color: white;
        }}

        QPushButton[class="warning"]:hover {{
            background: {StyleManager.WARNING_DARK};
        }}

        /* Info Button */
        QPushButton[class="info"] {{
            background: {StyleManager.INFO_COLOR};
            border: 1px solid {StyleManager.INFO_DARK};
            color: white;
        }}

        QPushButton[class="info"]:hover {{
            background: {StyleManager.INFO_DARK};
        }}

        /* GroupBox Styles */
        QGroupBox {{
            font-weight: 700;
            font-size: 14px;
            border: 1px solid {StyleManager.NEUTRAL_MEDIUM};
            border-radius: 8px;
            margin-top: 16px;
            padding-top: 24px;
            background: {StyleManager.BACKGROUND_COLOR};
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 5px 10px;
            color: {StyleManager.PRIMARY_COLOR};
        }}

        /* Text Input Styles */
        QLineEdit, QTextEdit {{
            border: 1px solid {StyleManager.NEUTRAL_MEDIUM};
            border-radius: 6px;
            padding: 8px 12px;
            background: {StyleManager.BACKGROUND_COLOR};
            selection-background-color: {StyleManager.PRIMARY_COLOR}40;
            font-size: 13px;
            color: {StyleManager.TEXT_COLOR};
        }}

        QLineEdit:focus, QTextEdit:focus {{
            border-color: {StyleManager.PRIMARY_COLOR};
            background: {StyleManager.BACKGROUND_COLOR};
        }}

        /* Table Styles */
        QTableWidget {{
            gridline-color: {StyleManager.NEUTRAL_MEDIUM};
            background: {StyleManager.BACKGROUND_COLOR};
            alternate-background-color: {StyleManager.NEUTRAL_LIGHT};
            border: 1px solid {StyleManager.NEUTRAL_MEDIUM};
            border-radius: 8px;
            selection-background-color: {StyleManager.PRIMARY_COLOR}20;
            selection-color: {StyleManager.PRIMARY_COLOR};
        }}

        QTableWidget::item {{
            padding: 6px;
            border-bottom: 1px solid {StyleManager.NEUTRAL_MEDIUM}40;
        }}

        QTableWidget::item:selected {{
            background: {StyleManager.PRIMARY_COLOR}20;
            color: {StyleManager.PRIMARY_DARK};
            font-weight: 600;
        }}

        QHeaderView::section {{
            background: {StyleManager.PRIMARY_COLOR};
            padding: 8px;
            border: none;
            font-weight: 600;
            color: white;
        }}

        /* Progress Bar */
        QProgressBar {{
            border: 1px solid {StyleManager.NEUTRAL_MEDIUM};
            border-radius: 4px;
            text-align: center;
            background: {StyleManager.NEUTRAL_LIGHT};
            height: 14px;
            color: {StyleManager.TEXT_COLOR};
        }}

        QProgressBar::chunk {{
            background: {StyleManager.PRIMARY_COLOR};
            border-radius: 3px;
        }}

        /* Status Bar */
        QStatusBar {{
            background: {StyleManager.NEUTRAL_LIGHT};
            border-top: 1px solid {StyleManager.NEUTRAL_MEDIUM};
            color: {StyleManager.TEXT_COLOR};
        }}

        /* Menu Styles */
        QMenuBar {{
            background: {StyleManager.BACKGROUND_COLOR};
            border-bottom: 1px solid {StyleManager.NEUTRAL_MEDIUM};
            color: {StyleManager.TEXT_COLOR};
        }}

        QMenuBar::item {{
            padding: 6px 10px;
            background: transparent;
            border-radius: 4px;
        }}

        QMenuBar::item:selected {{
            background: {StyleManager.PRIMARY_COLOR}20;
            color: {StyleManager.PRIMARY_COLOR};
        }}

        QMenu {{
            background: {StyleManager.BACKGROUND_COLOR};
            border: 1px solid {StyleManager.NEUTRAL_MEDIUM};
            border-radius: 6px;
            padding: 4px;
        }}

        QMenu::item {{
            padding: 8px 16px;
            border-radius: 4px;
        }}

        QMenu::item:selected {{
            background: {StyleManager.PRIMARY_COLOR}20;
            color: {StyleManager.PRIMARY_COLOR};
        }}

        /* Scrollbar Styles */
        QScrollBar:vertical {{
            background: {StyleManager.NEUTRAL_LIGHT};
            width: 10px;
            border-radius: 5px;
        }}

        QScrollBar::handle:vertical {{
            background: {StyleManager.NEUTRAL_MEDIUM};
            border-radius: 5px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {StyleManager.PRIMARY_COLOR}60;
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        /* ComboBox Styles */
        QComboBox {{
            border: 1px solid {StyleManager.NEUTRAL_MEDIUM};
            border-radius: 6px;
            padding: 8px 12px;
            background: {StyleManager.BACKGROUND_COLOR};
            min-width: 6em;
        }}

        QComboBox:focus {{
            border-color: {StyleManager.PRIMARY_COLOR};
        }}

        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}

        /* Checkbox Styles */
        QCheckBox {{
            spacing: 8px;
        }}

        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 1px solid {StyleManager.NEUTRAL_MEDIUM};
            border-radius: 4px;
            background: {StyleManager.BACKGROUND_COLOR};
        }}

        QCheckBox::indicator:checked {{
            background: {StyleManager.PRIMARY_COLOR};
            border-color: {StyleManager.PRIMARY_COLOR};
        }}

        QCheckBox::indicator:hover {{
            border-color: {StyleManager.PRIMARY_COLOR};
        }}
        """

    @staticmethod
    def apply_shadow_effect(widget, blur_radius=6, offset=(0, 2), color=None):
        """Add shadow effect to a widget"""
        if color is None:
            color = QColor(0, 0, 0, 20)  # Natural shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blur_radius)
        shadow.setXOffset(offset[0])
        shadow.setYOffset(offset[1])
        shadow.setColor(color)
        widget.setGraphicsEffect(shadow)

    @staticmethod
    def create_button(text, button_class="", icon=None):
        """Create a styled button with optional icon"""
        button = QPushButton(text)
        if button_class:
            button.setProperty("class", button_class)
        
        if icon:
            button.setText(f"{icon} {text}")
        
        StyleManager.apply_shadow_effect(button, blur_radius=4)
        return button

    @staticmethod
    def create_card(title="", content_widget=None, icon=None):
        """Create a card container with optional title and icon"""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setFrameShadow(QFrame.Shadow.Raised)
        card.setStyleSheet(f"""
            QFrame {{
                background: {StyleManager.BACKGROUND_COLOR};
                border: 1px solid {StyleManager.NEUTRAL_MEDIUM};
                border-radius: 8px;
                padding: 16px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        if title:
            header = QHBoxLayout()
            if icon:
                icon_label = QLabel(icon)
                icon_label.setStyleSheet(f"""
                    font-size: 16px;
                    color: {StyleManager.PRIMARY_COLOR};
                    margin-right: 8px;
                """)
                header.addWidget(icon_label)
            
            title_label = QLabel(title)
            title_label.setStyleSheet(f"""
                font-size: 16px;
                font-weight: bold;
                color: {StyleManager.PRIMARY_COLOR};
            """)
            header.addWidget(title_label)
            header.addStretch()
            layout.addLayout(header)
            
            # Add separator
            separator = QFrame()
            separator.setFrameShape(QFrame.Shape.HLine)
            separator.setFrameShadow(QFrame.Shadow.Sunken)
            separator.setStyleSheet(f"background-color: {StyleManager.NEUTRAL_MEDIUM};")
            layout.addWidget(separator)
        
        if content_widget:
            layout.addWidget(content_widget)
        
        StyleManager.apply_shadow_effect(card)
        return card

    @staticmethod
    def create_stat_card(icon, title, value, color=PRIMARY_COLOR):
        """Create a simplified statistic card"""
        card = QFrame()
        card.setFixedHeight(60)  # 减小高度
        card.setStyleSheet(f"""
            QFrame {{
                background: white;
                border-radius: 8px;
                border-left: 4px solid {color};
            }}
        """)
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(10, 5, 10, 5)  # 减小内边距
        
        # 简化图标显示
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"""
            font-size: 20px;
            color: {color};
            background: {color}10;
            border-radius: 15px;
            min-width: 30px;
            min-height: 30px;
            padding: 2px;
        """)
        
        # 创建包含数值和标题的容器
        content_layout = QHBoxLayout()
        content_layout.setSpacing(5)
        content_layout.setContentsMargins(5, 0, 0, 0)
        
        # 大数值标签
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            font-size: 20px;
            font-weight: bold;
            color: {color};
            margin-right: 5px;
        """)
        
        # 标题标签
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 12px;
            color: {StyleManager.NEUTRAL_DARK};
        """)
        
        content_layout.addWidget(value_label)
        content_layout.addWidget(title_label)
        content_layout.addStretch()
        
        # 将所有元素添加到主布局
        layout.addWidget(icon_label)
        layout.addLayout(content_layout)
        
        # 添加轻微阴影效果
        StyleManager.apply_shadow_effect(card, blur_radius=5, offset=(0, 2))
        
        # 存储值标签以便后续更新
        card.value_label = value_label
        return card


class Config:
    """配置管理类"""
    
    def __init__(self, config_file: str = "team_manager_config.json"):
        self.config_file = config_file
        self.default_config = {
            "api": {
                "base_url": "https://app.augmentcode.com/api",
                "headers": {
                    "accept": "*/*",
                    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                    "cache-control": "no-cache",
                    "pragma": "no-cache",
                    "priority": "u=1, i",
                    "sec-ch-ua": "\"Chromium\";v=\"136\", \"Microsoft Edge\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "\"Windows\"",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
                    "cookie": "_ga=GA1.1.1047401105.1748968739; vector_visitor_id=16cd1864-ab50-42c7-9906-0c9e4db2574d; ph_phc_TXdpocbGVeZVm5VJmAsHTMrCofBQu3e0kN8HGMNGTVW_posthog=%7B%22distinct_id%22%3A%2201973d97-58b1-7263-bfe3-cd1a606c05e4%22%2C%22%24sesid%22%3A%5B1749438152506%2C%22019752a3-bf26-7e4c-912e-231f39529e65%22%2C1749438152486%5D%7D; _ga_J5WQ9TVV7R=GS2.1.s1749438152$o2$g0$t1749438154$j58$l0$h0; ajs_user_id=ea900e8a-0a8b-4b3d-aa82-aefcd908f3fd; ajs_anonymous_id=a308fa9a-ccf9-421e-b035-15545527948a; _session=eyJvYXV0aDI6c3RhdGUiOiJ2ZHJwY1ZpdEk5bTl4RGJrbnIxb1A5dUE4SWFGa0NIdkNkcFZWak5ZX1B3Iiwib2F1dGgyOmNvZGVWZXJpZmllciI6IjJRTHU1d0g0UDVCLVRqb1BoWGNnYlM1TkFFb001dC1WeUJhQUhTRUtoM2ciLCJ1c2VyIjp7InVzZXJJZCI6ImVhOTAwZThhLTBhOGItNGIzZC1hYTgyLWFlZmNkOTA4ZjNmZCIsInRlbmFudElkIjoiNTFmZWZhYzY3MmU4MjUxMDRlYTI2MWQ2MzQxOGQwNzAiLCJ0ZW5hbnROYW1lIjoiaTAtdmFuZ3VhcmQzIiwic2hhcmROYW1lc3BhY2UiOiJpMCIsImVtYWlsIjoidWltbTgyMTcwNDZAb3V0bG9vay5jb20iLCJyb2xlcyI6W10sImNyZWF0ZWRBdCI6MTc0OTkwMzY0ODQ5MSwic2Vzc2lvbklkIjoiZjllMWNiM2UtM2VmNy00MmYzLThjMzEtMTZiNzk2MWQwMjNkIn19.4erGj14zvxI6oA7H8ecj6YnpCFrZTq1zRKHHpXVfhxY; _gcl_au=1.1.252217321.1748968739.1046711564.1749903758.1749903758; _ga_F6GPDJDCJY=GS2.1.s1749903587$o47$g1$t1749903945$j59$l0$h0; ph_phc_Kc4h1nMQmkyKUo9uGYXOCt25GiiXwguFcnWr1Xhl6bW_posthog=%7B%22distinct_id%22%3A%22ea900e8a-0a8b-4b3d-aa82-aefcd908f3fd%22%2C%22%24sesid%22%3A%5B1749903962817%2C%2201976e64-496e-7ed2-bf60-531d36514bc6%22%2C1749903755630%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22https%3A%2F%2Faccounts.google.com%2F%22%2C%22u%22%3A%22https%3A%2F%2Fapp.augmentcode.com%2Faccount%2Fselect-plan%22%7D%7D",
                    "Referer": "https://app.augmentcode.com/account/subscription",
                    "Referrer-Policy": "strict-origin-when-cross-origin"
                }
            },
            "ui": {
                "theme": "light",
                "font_size": 10,
                "auto_refresh": True,
                "refresh_interval": 30
            },
            "features": {
                "batch_operations": True,
                "email_validation": True,
                "auto_save": True
            }
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 合并默认配置，确保所有必要的键都存在
                return self._merge_config(self.default_config, config)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                return self.default_config.copy()
        return self.default_config.copy()
    
    def save_config(self) -> bool:
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def _merge_config(self, default: Dict, user: Dict) -> Dict:
        """递归合并配置"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, path: str, default=None):
        """获取配置值，支持点分隔路径"""
        keys = path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def set(self, path: str, value):
        """设置配置值，支持点分隔路径"""
        keys = path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value


class APIClient:
    """API客户端类"""
    
    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        headers = self.config.get('api.headers', {}).copy()
        # 为POST请求添加content-type
        if 'content-type' not in headers:
            headers['content-type'] = 'application/json'
        return headers
    
    def validate_email(self, email: str) -> bool:
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def get_team_data(self) -> Tuple[bool, Any]:
        """获取团队数据"""
        try:
            url = f"{self.config.get('api.base_url')}/team"
            headers = self._get_headers()

            # 调试信息：打印请求详情
            print(f"🔍 调试信息 - 请求URL: {url}")
            print(f"🔍 调试信息 - 请求头数量: {len(headers)}")

            # 检查Cookie是否存在
            cookie_value = headers.get('cookie', '')
            if cookie_value:
                print(f"🔍 调试信息 - Cookie长度: {len(cookie_value)} 字符")
                print(f"🔍 调试信息 - Cookie前50字符: {cookie_value[:50]}...")
                # 检查关键的认证字段
                if '_session=' in cookie_value:
                    print("✅ 调试信息 - 发现 _session 字段")
                else:
                    print("❌ 调试信息 - 缺少 _session 字段")
            else:
                print("❌ 调试信息 - Cookie为空")

            response = self.session.get(url, headers=headers, timeout=30)

            print(f"🔍 调试信息 - 响应状态码: {response.status_code}")
            print(f"🔍 调试信息 - 响应头: {dict(response.headers)}")

            if response.status_code == 200:
                try:
                    json_data = response.json()
                    print(f"✅ 调试信息 - 成功获取JSON数据，数据类型: {type(json_data)}")
                    if isinstance(json_data, dict):
                        print(f"✅ 调试信息 - JSON数据键: {list(json_data.keys())}")
                    return True, json_data
                except Exception as json_error:
                    print(f"❌ 调试信息 - JSON解析失败: {str(json_error)}")
                    print(f"❌ 调试信息 - 响应内容: {response.text[:500]}...")
                    return False, f"JSON解析失败: {str(json_error)}"
            else:
                error_msg = f"请求失败，状态码: {response.status_code}"
                print(f"❌ 调试信息 - {error_msg}")
                print(f"❌ 调试信息 - 响应内容: {response.text[:500]}...")
                return False, f"{error_msg}\n响应内容: {response.text[:200]}..."
        except Exception as e:
            error_msg = f"网络错误: {str(e)}"
            print(f"❌ 调试信息 - {error_msg}")
            return False, error_msg
    
    def invite_members(self, emails: List[str]) -> Tuple[bool, str]:
        """批量邀请成员"""
        try:
            url = f"{self.config.get('api.base_url')}/team/invite"
            headers = self._get_headers()
            data = {"emails": emails}
            
            response = self.session.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                return True, "邀请发送成功"
            else:
                return False, f"邀请失败，状态码: {response.status_code}\n响应: {response.text}"
        except Exception as e:
            return False, f"网络错误: {str(e)}"
    
    def delete_member(self, member_id: str) -> Tuple[bool, str]:
        """删除单个成员或邀请"""
        try:
            url = f"{self.config.get('api.base_url')}/team/invite/{member_id}"
            headers = self._get_headers()

            response = self.session.delete(url, headers=headers, timeout=30)

            if response.status_code == 200:
                return True, "删除成功"
            else:
                return False, f"删除失败，状态码: {response.status_code}"
        except Exception as e:
            return False, f"网络错误: {str(e)}"

    def put_user_on_community_plan(self) -> Tuple[bool, str]:
        """将登录账号改为 community plan"""
        try:
            url = f"{self.config.get('api.base_url')}/put-user-on-plan"
            headers = self._get_headers()
            data = {"planId": "orb_community_plan"}

            response = self.session.post(url, headers=headers, json=data, timeout=30)

            if response.status_code == 200:
                return True, "账号已成功切换到 Community Plan"
            else:
                return False, f"切换失败，状态码: {response.status_code}\n响应: {response.text}"
        except Exception as e:
            return False, f"网络错误: {str(e)}"

    def put_user_on_max_plan(self) -> Tuple[bool, str]:
        """将登录账号改为 max plan"""
        try:
            url = f"{self.config.get('api.base_url')}/put-user-on-plan"
            headers = self._get_headers()
            data = {"planId": "orb_max_plan"}

            response = self.session.post(url, headers=headers, json=data, timeout=30)

            if response.status_code == 200:
                return True, "账号已成功切换到 Max Plan"
            else:
                return False, f"切换失败，状态码: {response.status_code}\n响应: {response.text}"
        except Exception as e:
            return False, f"网络错误: {str(e)}"

    def put_user_on_plan(self, plan_id: str) -> Tuple[bool, str]:
        """将登录账号改为指定计划"""
        try:
            url = f"{self.config.get('api.base_url')}/put-user-on-plan"
            headers = self._get_headers()
            data = {"planId": plan_id}

            response = self.session.post(url, headers=headers, json=data, timeout=30)

            if response.status_code == 200:
                return True, f"账号已成功切换到 {plan_id}"
            else:
                return False, f"切换失败，状态码: {response.status_code}\n响应: {response.text}"
        except Exception as e:
            return False, f"网络错误: {str(e)}"


class WorkerThread(QThread):
    """工作线程类，用于执行耗时操作"""
    
    finished = pyqtSignal(bool, str, object)  # success, message, data
    progress = pyqtSignal(int, str)  # progress, status
    
    def __init__(self, api_client: APIClient, operation: str, **kwargs):
        super().__init__()
        self.api_client = api_client
        self.operation = operation
        self.kwargs = kwargs
    
    def run(self):
        """执行操作"""
        try:
            if self.operation == "get_team_data":
                success, result = self.api_client.get_team_data()
                self.finished.emit(success, str(result) if not success else "", result if success else None)
            
            elif self.operation == "invite_members":
                emails = self.kwargs.get('emails', [])
                success, message = self.api_client.invite_members(emails)
                self.finished.emit(success, message, None)
            
            elif self.operation == "delete_member":
                member_id = self.kwargs.get('member_id')
                success, message = self.api_client.delete_member(member_id)
                self.finished.emit(success, message, None)
            
            elif self.operation == "batch_delete":
                member_ids = self.kwargs.get('member_ids', [])
                success_count = 0
                failed_count = 0
                failed_ids = []

                for i, member_id in enumerate(member_ids):
                    self.progress.emit(int((i + 1) / len(member_ids) * 100), f"删除成员 {i + 1}/{len(member_ids)}")

                    success, message = self.api_client.delete_member(member_id)
                    if success:
                        success_count += 1
                    else:
                        failed_count += 1
                        failed_ids.append(member_id)

                result_message = f"批量删除完成：成功 {success_count} 个，失败 {failed_count} 个"
                if failed_ids:
                    result_message += f"\n失败的ID: {', '.join(failed_ids)}"

                self.finished.emit(failed_count == 0, result_message, None)

            elif self.operation == "put_user_on_community_plan":
                success, message = self.api_client.put_user_on_community_plan()
                self.finished.emit(success, message, None)

            elif self.operation == "put_user_on_max_plan":
                success, message = self.api_client.put_user_on_max_plan()
                self.finished.emit(success, message, None)

            elif self.operation == "put_user_on_plan":
                plan_id = self.kwargs.get('plan_id', 'orb_community_plan')
                success, message = self.api_client.put_user_on_plan(plan_id)
                self.finished.emit(success, message, None)
            
        except Exception as e:
            self.finished.emit(False, f"操作异常: {str(e)}", None)


class CustomMessageBox(QWidget):
    """自定义消息框，确保内容完整显示"""

    def __init__(self, title, message, msg_type="info", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self.setModal(True)
        self.init_ui(title, message, msg_type)

    def init_ui(self, title, message, msg_type):
        """初始化消息框界面"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 根据类型设置图标和颜色
        if msg_type == "success":
            icon = "✅"
            color = StyleManager.SUCCESS_COLOR
        elif msg_type == "error":
            icon = "❌"
            color = StyleManager.DANGER_COLOR
        elif msg_type == "warning":
            icon = "⚠️"
            color = StyleManager.WARNING_COLOR
        else:
            icon = "ℹ️"
            color = StyleManager.PRIMARY_COLOR

        # 标题区域
        title_layout = QHBoxLayout()
        title_icon = QLabel(icon)
        title_icon.setStyleSheet("font-size: 24px;")
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                font-weight: bold;
                color: {color};
                margin-left: 10px;
            }}
        """)
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # 消息内容
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        msg_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                line-height: 1.5;
                padding: 10px;
                background: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }
        """)
        msg_label.setMinimumWidth(400)
        msg_label.setMaximumWidth(600)
        layout.addWidget(msg_label)

        # 按钮区域
        button_layout = QHBoxLayout()
        ok_btn = StyleManager.create_button("确定", "primary")
        ok_btn.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(ok_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # 根据内容调整大小
        self.adjustSize()
        self.setMinimumSize(450, 200)

        # 应用样式和阴影
        self.setStyleSheet(f"""
            QWidget {{
                background: white;
                border-radius: 12px;
            }}
        """)
        StyleManager.apply_shadow_effect(self, blur_radius=20, offset=(0, 10))

    def accept(self):
        """确定按钮点击事件"""
        self.close()

    @staticmethod
    def show_info(parent, title, message):
        """显示信息消息框"""
        dialog = CustomMessageBox(title, message, "info", parent)
        dialog.show()
        return dialog

    @staticmethod
    def show_success(parent, title, message):
        """显示成功消息框"""
        dialog = CustomMessageBox(title, message, "success", parent)
        dialog.show()
        return dialog

    @staticmethod
    def show_warning(parent, title, message):
        """显示警告消息框"""
        dialog = CustomMessageBox(title, message, "warning", parent)
        dialog.show()
        return dialog

    @staticmethod
    def show_error(parent, title, message):
        """显示错误消息框"""
        dialog = CustomMessageBox(title, message, "error", parent)
        dialog.show()
        return dialog


class CustomConfirmDialog(QWidget):
    """自定义确认对话框"""

    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.result = False
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self.setModal(True)
        self.init_ui(title, message)

    def init_ui(self, title, message):
        """初始化确认对话框界面"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 标题区域
        title_layout = QHBoxLayout()
        title_icon = QLabel("❓")
        title_icon.setStyleSheet("font-size: 24px;")
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                font-weight: bold;
                color: {StyleManager.WARNING_COLOR};
                margin-left: 10px;
            }}
        """)
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # 消息内容
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        msg_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                line-height: 1.5;
                padding: 10px;
                background: #fff3cd;
                border-radius: 8px;
                border: 1px solid #ffeaa7;
                color: #856404;
            }
        """)
        msg_label.setMinimumWidth(400)
        msg_label.setMaximumWidth(600)
        layout.addWidget(msg_label)

        # 按钮区域
        button_layout = QHBoxLayout()
        cancel_btn = StyleManager.create_button("取消", "")
        cancel_btn.clicked.connect(self.reject)

        confirm_btn = StyleManager.create_button("确定", "warning")
        confirm_btn.clicked.connect(self.accept)

        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(confirm_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # 根据内容调整大小
        self.adjustSize()
        self.setMinimumSize(450, 200)

        # 应用样式和阴影
        self.setStyleSheet(f"""
            QWidget {{
                background: white;
                border-radius: 12px;
            }}
        """)
        StyleManager.apply_shadow_effect(self, blur_radius=20, offset=(0, 10))

    def accept(self):
        """确定按钮点击事件"""
        self.result = True
        self.close()

    def reject(self):
        """取消按钮点击事件"""
        self.result = False
        self.close()

    @staticmethod
    def ask_confirmation(parent, title, message):
        """显示确认对话框并返回结果"""
        dialog = CustomConfirmDialog(title, message, parent)
        dialog.exec()
        return dialog.result


class PendingEmailsDialog(QWidget):
    """未接受邮箱列表弹窗"""

    def __init__(self, emails: List[str], parent=None):
        super().__init__(parent)
        self.emails = emails
        self.setWindowTitle("📧 未接受邀请的邮箱列表")
        self.setGeometry(300, 200, 600, 500)
        self.setMinimumSize(500, 400)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)
        self.init_ui()

    def init_ui(self):
        """初始化弹窗界面"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 标题区域
        title_layout = QHBoxLayout()
        title_icon = QLabel("📧")
        title_icon.setStyleSheet("font-size: 24px;")
        title_label = QLabel(f"未接受邀请的邮箱列表 ({len(self.emails)} 个)")
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {StyleManager.PRIMARY_COLOR};
                margin-left: 10px;
            }}
        """)
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        main_layout.addLayout(title_layout)

        # 邮箱列表显示区域
        list_group = QGroupBox("邮箱地址")
        list_layout = QVBoxLayout()
        list_layout.setSpacing(10)

        # 创建文本编辑器显示邮箱列表
        self.email_text = QTextEdit()
        self.email_text.setPlainText('\n'.join(self.emails))
        self.email_text.setReadOnly(True)
        self.email_text.setMinimumHeight(250)
        self.email_text.setStyleSheet(f"""
            QTextEdit {{
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                line-height: 1.5;
                border: 2px solid {StyleManager.NEUTRAL_MEDIUM};
                border-radius: 8px;
                padding: 10px;
                background: {StyleManager.BACKGROUND_COLOR};
                selection-background-color: {StyleManager.PRIMARY_COLOR}40;
            }}
        """)
        list_layout.addWidget(self.email_text)

        # 统计信息
        stats_label = QLabel(f"总计: {len(self.emails)} 个邮箱地址")
        stats_label.setStyleSheet(f"""
            QLabel {{
                color: {StyleManager.NEUTRAL_DARK};
                font-size: 12px;
                padding: 5px;
                background: {StyleManager.NEUTRAL_LIGHT};
                border-radius: 4px;
            }}
        """)
        list_layout.addWidget(stats_label)

        list_group.setLayout(list_layout)
        main_layout.addWidget(list_group)

        # 操作按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        # 全选按钮
        select_all_btn = StyleManager.create_button("📋 全选", "primary")
        select_all_btn.clicked.connect(self.select_all_emails)
        select_all_btn.setToolTip("选择所有邮箱地址")

        # 复制按钮
        copy_btn = StyleManager.create_button("📄 复制到剪贴板", "success")
        copy_btn.clicked.connect(self.copy_to_clipboard)
        copy_btn.setToolTip("复制所有邮箱地址到剪贴板")

        # 导出按钮
        export_btn = StyleManager.create_button("💾 导出到文件", "info")
        export_btn.clicked.connect(self.export_to_file)
        export_btn.setToolTip("导出邮箱列表到文本文件")

        # 关闭按钮
        close_btn = StyleManager.create_button("❌ 关闭", "danger")
        close_btn.clicked.connect(self.close)

        button_layout.addWidget(select_all_btn)
        button_layout.addWidget(copy_btn)
        button_layout.addWidget(export_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # 应用样式
        self.setStyleSheet(f"""
            QWidget {{
                background: {StyleManager.BACKGROUND_COLOR};
            }}
        """)

        # 添加阴影效果
        StyleManager.apply_shadow_effect(self, blur_radius=20, offset=(0, 10))

    def select_all_emails(self):
        """全选所有邮箱地址"""
        self.email_text.selectAll()

    def copy_to_clipboard(self):
        """复制邮箱列表到剪贴板"""
        clipboard = QApplication.clipboard()
        email_text = '\n'.join(self.emails)
        clipboard.setText(email_text)

        # 显示成功提示
        CustomMessageBox.show_success(self, "复制成功",
                              f"已复制 {len(self.emails)} 个邮箱地址到剪贴板\n\n"
                              "每行一个邮箱，方便粘贴使用。")

    def export_to_file(self):
        """导出邮箱列表到文件"""
        from PyQt6.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出邮箱列表",
            f"pending_emails_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "文本文件 (*.txt);;所有文件 (*)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(self.emails))
                CustomMessageBox.show_success(self, "导出成功",
                                      f"邮箱列表已成功导出到:\n{file_path}")
            except Exception as e:
                CustomMessageBox.show_error(self, "导出失败", f"导出文件时发生错误:\n{str(e)}")


class ConfigDialog(QWidget):
    """配置对话框"""

    # 添加配置更改信号
    config_changed = pyqtSignal()

    def __init__(self, config: Config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("🔧 配置设置")
        self.setGeometry(200, 200, 900, 700)  # 增大窗口尺寸
        self.setMinimumSize(800, 600)  # 设置最小尺寸
        self.init_ui()
    
    def init_ui(self):
        """初始化现代化配置UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 标题区域
        title_label = QLabel("🔧 系统配置管理")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 15px;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                          stop: 0 #4facfe, stop: 1 #00f2fe);
                color: white;
                border-radius: 12px;
                margin-bottom: 10px;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # 创建标签页
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                background: white;
                margin-top: 5px;
            }
            QTabBar::tab {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-bottom: none;
                border-radius: 8px 8px 0 0;
                padding: 12px 20px;
                margin-right: 2px;
                font-weight: 600;
                font-size: 14px;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid white;
                color: #4facfe;
            }
            QTabBar::tab:hover {
                background: #e9ecef;
            }
        """)

        # API配置标签页
        api_tab = self.create_api_tab()
        tab_widget.addTab(api_tab, "🔗 API配置")

        # UI配置标签页
        ui_tab = self.create_ui_tab()
        tab_widget.addTab(ui_tab, "🎨 界面配置")

        # 功能配置标签页
        features_tab = self.create_features_tab()
        tab_widget.addTab(features_tab, "⚙️ 功能配置")

        # 高级配置标签页
        advanced_tab = self.create_advanced_tab()
        tab_widget.addTab(advanced_tab, "🔧 高级配置")

        main_layout.addWidget(tab_widget)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        save_btn = StyleManager.create_button("💾 保存配置", "success")
        save_btn.clicked.connect(self.save_config)

        reset_btn = StyleManager.create_button("🔄 重置默认", "warning")
        reset_btn.clicked.connect(self.reset_config)

        test_btn = StyleManager.create_button("🧪 测试连接", "primary")
        test_btn.clicked.connect(self.test_connection)

        close_btn = StyleManager.create_button("❌ 关闭", "danger")
        close_btn.clicked.connect(self.close)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(reset_btn)
        button_layout.addWidget(test_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
    
    def create_api_tab(self) -> QWidget:
        """创建API配置标签页"""
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # 创建内容widget
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)

        # API基础配置
        api_group = QGroupBox("🌐 API基础配置")
        api_layout = QFormLayout()
        api_layout.setSpacing(12)

        self.base_url_edit = QLineEdit(self.config.get('api.base_url', ''))
        self.base_url_edit.setPlaceholderText("https://app.augmentcode.com/api")
        api_layout.addRow("API基础URL:", self.base_url_edit)

        api_group.setLayout(api_layout)
        layout.addWidget(api_group)

        # Headers配置
        headers_group = QGroupBox("📋 请求头配置")
        headers_layout = QVBoxLayout()
        headers_layout.setSpacing(15)

        # Cookie配置（最重要的）
        cookie_section = QVBoxLayout()
        cookie_label = QLabel("🍪 Cookie (最重要的认证信息):")
        cookie_label.setStyleSheet("font-weight: bold; color: #e74c3c;")
        cookie_section.addWidget(cookie_label)

        self.cookie_edit = QTextEdit()
        self.cookie_edit.setFixedHeight(120)
        self.cookie_edit.setPlaceholderText("请粘贴从浏览器开发者工具中复制的完整Cookie...")
        self.cookie_edit.setPlainText(self.config.get('api.headers.cookie', ''))
        self.cookie_edit.setStyleSheet("""
            QTextEdit {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                border: 2px solid #e74c3c;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        # 添加Cookie变化监听
        self.cookie_edit.textChanged.connect(self.validate_cookie)
        cookie_section.addWidget(self.cookie_edit)

        # Cookie验证状态显示
        self.cookie_status_label = QLabel("Cookie状态: 未验证")
        self.cookie_status_label.setStyleSheet("""
            QLabel {
                padding: 8px;
                border-radius: 4px;
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                font-size: 12px;
            }
        """)
        cookie_section.addWidget(self.cookie_status_label)

        # Cookie帮助按钮
        cookie_help_layout = QHBoxLayout()
        cookie_help_btn = QPushButton("📖 Cookie获取帮助")
        cookie_help_btn.clicked.connect(self.show_cookie_help)
        cookie_validate_btn = QPushButton("🔍 验证Cookie")
        cookie_validate_btn.clicked.connect(self.validate_cookie_detailed)

        cookie_help_layout.addWidget(cookie_help_btn)
        cookie_help_layout.addWidget(cookie_validate_btn)
        cookie_help_layout.addStretch()
        cookie_section.addLayout(cookie_help_layout)

        headers_layout.addLayout(cookie_section)

        # 其他重要headers
        other_headers_layout = QFormLayout()
        other_headers_layout.setSpacing(10)

        self.user_agent_edit = QLineEdit(self.config.get('api.headers.sec-ch-ua', ''))
        self.user_agent_edit.setPlaceholderText('"Chromium";v="136", "Microsoft Edge";v="136"')
        other_headers_layout.addRow("User Agent (sec-ch-ua):", self.user_agent_edit)

        self.referer_edit = QLineEdit(self.config.get('api.headers.Referer', ''))
        self.referer_edit.setPlaceholderText("https://app.augmentcode.com/")
        other_headers_layout.addRow("Referer:", self.referer_edit)

        self.accept_edit = QLineEdit(self.config.get('api.headers.accept', '*/*'))
        other_headers_layout.addRow("Accept:", self.accept_edit)

        self.accept_language_edit = QLineEdit(self.config.get('api.headers.accept-language', 'zh-CN,zh;q=0.9'))
        other_headers_layout.addRow("Accept-Language:", self.accept_language_edit)

        headers_layout.addLayout(other_headers_layout)
        headers_group.setLayout(headers_layout)
        layout.addWidget(headers_group)

        # 配置状态显示
        status_group = QGroupBox("📊 配置状态")
        status_layout = QVBoxLayout()

        self.config_status_label = QLabel("配置状态: 未检测")
        self.config_status_label.setStyleSheet("""
            QLabel {
                padding: 10px;
                border-radius: 6px;
                background: #f8f9fa;
                border: 1px solid #dee2e6;
            }
        """)
        status_layout.addWidget(self.config_status_label)

        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        # 添加弹性空间
        layout.addStretch()
        content_widget.setLayout(layout)

        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)

        # 创建主容器
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        main_widget.setLayout(main_layout)

        return main_widget
    
    def create_ui_tab(self) -> QWidget:
        """创建UI配置标签页"""
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # 创建内容widget
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)

        # 界面外观设置
        appearance_group = QGroupBox("🎨 界面外观")
        appearance_layout = QFormLayout()
        appearance_layout.setSpacing(12)

        # 主题选择
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["light", "dark", "auto"])
        self.theme_combo.setCurrentText(self.config.get('ui.theme', 'light'))
        appearance_layout.addRow("界面主题:", self.theme_combo)

        # 字体大小
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setSuffix(" px")
        self.font_size_spin.setValue(self.config.get('ui.font_size', 12))
        appearance_layout.addRow("字体大小:", self.font_size_spin)

        # 窗口透明度
        self.opacity_spin = QSpinBox()
        self.opacity_spin.setRange(70, 100)
        self.opacity_spin.setSuffix(" %")
        self.opacity_spin.setValue(self.config.get('ui.opacity', 100))
        appearance_layout.addRow("窗口透明度:", self.opacity_spin)

        appearance_group.setLayout(appearance_layout)
        layout.addWidget(appearance_group)

        # 行为设置
        behavior_group = QGroupBox("⚙️ 行为设置")
        behavior_layout = QFormLayout()
        behavior_layout.setSpacing(12)

        # 自动刷新
        self.auto_refresh_check = QCheckBox()
        self.auto_refresh_check.setChecked(self.config.get('ui.auto_refresh', True))
        behavior_layout.addRow("启用自动刷新:", self.auto_refresh_check)

        # 刷新间隔
        self.refresh_interval_spin = QSpinBox()
        self.refresh_interval_spin.setRange(10, 600)
        self.refresh_interval_spin.setSuffix(" 秒")
        self.refresh_interval_spin.setValue(self.config.get('ui.refresh_interval', 30))
        behavior_layout.addRow("刷新间隔:", self.refresh_interval_spin)

        # 启动时最小化
        self.start_minimized_check = QCheckBox()
        self.start_minimized_check.setChecked(self.config.get('ui.start_minimized', False))
        behavior_layout.addRow("启动时最小化:", self.start_minimized_check)

        # 关闭到系统托盘
        self.close_to_tray_check = QCheckBox()
        self.close_to_tray_check.setChecked(self.config.get('ui.close_to_tray', False))
        behavior_layout.addRow("关闭到系统托盘:", self.close_to_tray_check)

        behavior_group.setLayout(behavior_layout)
        layout.addWidget(behavior_group)

        # 显示设置
        display_group = QGroupBox("📺 显示设置")
        display_layout = QFormLayout()
        display_layout.setSpacing(12)

        # 显示动画
        self.animations_check = QCheckBox()
        self.animations_check.setChecked(self.config.get('ui.animations', True))
        display_layout.addRow("启用动画效果:", self.animations_check)

        # 显示阴影
        self.shadows_check = QCheckBox()
        self.shadows_check.setChecked(self.config.get('ui.shadows', True))
        display_layout.addRow("显示阴影效果:", self.shadows_check)

        # 表格行数限制
        self.table_rows_spin = QSpinBox()
        self.table_rows_spin.setRange(50, 1000)
        self.table_rows_spin.setValue(self.config.get('ui.max_table_rows', 200))
        display_layout.addRow("表格最大行数:", self.table_rows_spin)

        display_group.setLayout(display_layout)
        layout.addWidget(display_group)

        # 添加弹性空间
        layout.addStretch()
        content_widget.setLayout(layout)

        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)

        # 创建主容器
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        main_widget.setLayout(main_layout)

        return main_widget
    
    def create_features_tab(self) -> QWidget:
        """创建功能配置标签页"""
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # 创建内容widget
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)

        # 核心功能设置
        core_group = QGroupBox("🔧 核心功能")
        core_layout = QFormLayout()
        core_layout.setSpacing(12)

        # 批量操作
        self.batch_ops_check = QCheckBox()
        self.batch_ops_check.setChecked(self.config.get('features.batch_operations', True))
        core_layout.addRow("启用批量操作:", self.batch_ops_check)

        # 邮箱验证
        self.email_validation_check = QCheckBox()
        self.email_validation_check.setChecked(self.config.get('features.email_validation', True))
        core_layout.addRow("邮箱格式验证:", self.email_validation_check)

        # 自动保存
        self.auto_save_check = QCheckBox()
        self.auto_save_check.setChecked(self.config.get('features.auto_save', True))
        core_layout.addRow("自动保存配置:", self.auto_save_check)

        # 数据导出
        self.data_export_check = QCheckBox()
        self.data_export_check.setChecked(self.config.get('features.data_export', True))
        core_layout.addRow("启用数据导出:", self.data_export_check)

        core_group.setLayout(core_layout)
        layout.addWidget(core_group)

        # 安全设置
        security_group = QGroupBox("🔒 安全设置")
        security_layout = QFormLayout()
        security_layout.setSpacing(12)

        # 操作确认
        self.confirm_operations_check = QCheckBox()
        self.confirm_operations_check.setChecked(self.config.get('security.confirm_operations', True))
        security_layout.addRow("危险操作确认:", self.confirm_operations_check)

        # 日志记录
        self.logging_check = QCheckBox()
        self.logging_check.setChecked(self.config.get('security.logging', True))
        security_layout.addRow("启用操作日志:", self.logging_check)

        # 备份配置
        self.backup_config_check = QCheckBox()
        self.backup_config_check.setChecked(self.config.get('security.backup_config', True))
        security_layout.addRow("自动备份配置:", self.backup_config_check)

        security_group.setLayout(security_layout)
        layout.addWidget(security_group)

        # 性能设置
        performance_group = QGroupBox("⚡ 性能设置")
        performance_layout = QFormLayout()
        performance_layout.setSpacing(12)

        # 请求超时
        self.request_timeout_spin = QSpinBox()
        self.request_timeout_spin.setRange(5, 120)
        self.request_timeout_spin.setSuffix(" 秒")
        self.request_timeout_spin.setValue(self.config.get('performance.request_timeout', 30))
        performance_layout.addRow("请求超时时间:", self.request_timeout_spin)

        # 重试次数
        self.retry_count_spin = QSpinBox()
        self.retry_count_spin.setRange(0, 10)
        self.retry_count_spin.setValue(self.config.get('performance.retry_count', 3))
        performance_layout.addRow("请求重试次数:", self.retry_count_spin)

        # 并发限制
        self.concurrent_limit_spin = QSpinBox()
        self.concurrent_limit_spin.setRange(1, 20)
        self.concurrent_limit_spin.setValue(self.config.get('performance.concurrent_limit', 5))
        performance_layout.addRow("并发请求限制:", self.concurrent_limit_spin)

        performance_group.setLayout(performance_layout)
        layout.addWidget(performance_group)

        # 添加弹性空间
        layout.addStretch()
        content_widget.setLayout(layout)

        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)

        # 创建主容器
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        main_widget.setLayout(main_layout)

        return main_widget

    def create_advanced_tab(self) -> QWidget:
        """创建高级配置标签页"""
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # 创建内容widget
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)

        # 调试设置
        debug_group = QGroupBox("🐛 调试设置")
        debug_layout = QFormLayout()
        debug_layout.setSpacing(12)

        # 调试模式
        self.debug_mode_check = QCheckBox()
        self.debug_mode_check.setChecked(self.config.get('debug.enabled', False))
        debug_layout.addRow("启用调试模式:", self.debug_mode_check)

        # 详细日志
        self.verbose_logging_check = QCheckBox()
        self.verbose_logging_check.setChecked(self.config.get('debug.verbose_logging', False))
        debug_layout.addRow("详细日志输出:", self.verbose_logging_check)

        # 保存请求日志
        self.save_requests_check = QCheckBox()
        self.save_requests_check.setChecked(self.config.get('debug.save_requests', False))
        debug_layout.addRow("保存请求日志:", self.save_requests_check)

        debug_group.setLayout(debug_layout)
        layout.addWidget(debug_group)

        # 网络设置
        network_group = QGroupBox("🌐 网络设置")
        network_layout = QFormLayout()
        network_layout.setSpacing(12)

        # 代理设置
        self.proxy_enabled_check = QCheckBox()
        self.proxy_enabled_check.setChecked(self.config.get('network.proxy.enabled', False))
        network_layout.addRow("启用代理:", self.proxy_enabled_check)

        self.proxy_host_edit = QLineEdit(self.config.get('network.proxy.host', ''))
        self.proxy_host_edit.setPlaceholderText("127.0.0.1")
        network_layout.addRow("代理主机:", self.proxy_host_edit)

        self.proxy_port_spin = QSpinBox()
        self.proxy_port_spin.setRange(1, 65535)
        self.proxy_port_spin.setValue(self.config.get('network.proxy.port', 8080))
        network_layout.addRow("代理端口:", self.proxy_port_spin)

        # SSL验证
        self.ssl_verify_check = QCheckBox()
        self.ssl_verify_check.setChecked(self.config.get('network.ssl_verify', True))
        network_layout.addRow("SSL证书验证:", self.ssl_verify_check)

        network_group.setLayout(network_layout)
        layout.addWidget(network_group)

        # 数据管理
        data_group = QGroupBox("💾 数据管理")
        data_layout = QVBoxLayout()
        data_layout.setSpacing(15)

        # 配置文件路径显示
        config_path_layout = QHBoxLayout()
        config_path_label = QLabel("配置文件路径:")
        self.config_path_display = QLineEdit(self.config.config_file)
        self.config_path_display.setReadOnly(True)
        browse_config_btn = QPushButton("📁 浏览")
        browse_config_btn.clicked.connect(self.browse_config_file)

        config_path_layout.addWidget(config_path_label)
        config_path_layout.addWidget(self.config_path_display)
        config_path_layout.addWidget(browse_config_btn)
        data_layout.addLayout(config_path_layout)

        # 操作按钮
        data_buttons_layout = QHBoxLayout()

        export_config_btn = QPushButton("📤 导出配置")
        export_config_btn.clicked.connect(self.export_config)

        import_config_btn = QPushButton("📥 导入配置")
        import_config_btn.clicked.connect(self.import_config)

        clear_cache_btn = QPushButton("🧹 清理缓存")
        clear_cache_btn.clicked.connect(self.clear_cache)

        data_buttons_layout.addWidget(export_config_btn)
        data_buttons_layout.addWidget(import_config_btn)
        data_buttons_layout.addWidget(clear_cache_btn)
        data_buttons_layout.addStretch()

        data_layout.addLayout(data_buttons_layout)
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)

        # 添加弹性空间
        layout.addStretch()
        content_widget.setLayout(layout)

        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)

        # 创建主容器
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        main_widget.setLayout(main_layout)

        return main_widget

    def save_config(self):
        """保存配置"""
        try:
            # 保存API配置
            self.config.set('api.base_url', self.base_url_edit.text())
            self.config.set('api.headers.cookie', self.cookie_edit.toPlainText())
            self.config.set('api.headers.sec-ch-ua', self.user_agent_edit.text())
            self.config.set('api.headers.Referer', self.referer_edit.text())
            self.config.set('api.headers.accept', self.accept_edit.text())
            self.config.set('api.headers.accept-language', self.accept_language_edit.text())

            # 保存UI配置
            self.config.set('ui.theme', self.theme_combo.currentText())
            self.config.set('ui.font_size', self.font_size_spin.value())
            self.config.set('ui.opacity', self.opacity_spin.value())
            self.config.set('ui.auto_refresh', self.auto_refresh_check.isChecked())
            self.config.set('ui.refresh_interval', self.refresh_interval_spin.value())
            self.config.set('ui.start_minimized', self.start_minimized_check.isChecked())
            self.config.set('ui.close_to_tray', self.close_to_tray_check.isChecked())
            self.config.set('ui.animations', self.animations_check.isChecked())
            self.config.set('ui.shadows', self.shadows_check.isChecked())
            self.config.set('ui.max_table_rows', self.table_rows_spin.value())

            # 保存功能配置
            self.config.set('features.batch_operations', self.batch_ops_check.isChecked())
            self.config.set('features.email_validation', self.email_validation_check.isChecked())
            self.config.set('features.auto_save', self.auto_save_check.isChecked())
            self.config.set('features.data_export', self.data_export_check.isChecked())

            # 保存安全配置
            self.config.set('security.confirm_operations', self.confirm_operations_check.isChecked())
            self.config.set('security.logging', self.logging_check.isChecked())
            self.config.set('security.backup_config', self.backup_config_check.isChecked())

            # 保存性能配置
            self.config.set('performance.request_timeout', self.request_timeout_spin.value())
            self.config.set('performance.retry_count', self.retry_count_spin.value())
            self.config.set('performance.concurrent_limit', self.concurrent_limit_spin.value())

            # 保存高级配置
            self.config.set('debug.enabled', self.debug_mode_check.isChecked())
            self.config.set('debug.verbose_logging', self.verbose_logging_check.isChecked())
            self.config.set('debug.save_requests', self.save_requests_check.isChecked())

            # 保存网络配置
            self.config.set('network.proxy.enabled', self.proxy_enabled_check.isChecked())
            self.config.set('network.proxy.host', self.proxy_host_edit.text())
            self.config.set('network.proxy.port', self.proxy_port_spin.value())
            self.config.set('network.ssl_verify', self.ssl_verify_check.isChecked())

            # 保存到文件
            if self.config.save_config():
                print("✅ 配置保存成功！")
                self.update_config_status("✅ 配置已保存", StyleManager.SUCCESS_COLOR)
                # 发射配置更改信号
                self.config_changed.emit()
            else:
                print("❌ 配置保存失败！")
                self.update_config_status("❌ 保存失败", StyleManager.DANGER_COLOR)

        except Exception as e:
            print(f"❌ 保存配置时发生错误: {str(e)}")
            self.update_config_status(f"❌ 保存错误: {str(e)}", StyleManager.DANGER_COLOR)

    def reset_config(self):
        """重置为默认配置"""
        print("⚠️ 重置配置为默认值")
        self.config.config = self.config.default_config.copy()
        self.config.save_config()
        print("✅ 配置已重置为默认值！")
        self.update_config_status("✅ 配置已重置", StyleManager.SUCCESS_COLOR)
        # 发射配置更改信号
        self.config_changed.emit()
        self.close()

    def test_connection(self):
        """测试API连接 - 增强版调试"""
        try:
            # 临时保存当前配置
            temp_config = Config()
            temp_config.config = self.config.config.copy()

            # 更新临时配置
            temp_config.set('api.base_url', self.base_url_edit.text())
            temp_config.set('api.headers.cookie', self.cookie_edit.toPlainText())
            temp_config.set('api.headers.sec-ch-ua', self.user_agent_edit.text())
            temp_config.set('api.headers.Referer', self.referer_edit.text())
            temp_config.set('api.headers.accept', self.accept_edit.text())
            temp_config.set('api.headers.accept-language', self.accept_language_edit.text())

            # 显示详细的配置检查信息
            cookie_text = self.cookie_edit.toPlainText().strip()
            base_url = self.base_url_edit.text().strip()

            print("\n" + "="*60)
            print("🔧 配置连接测试开始")
            print("="*60)
            print(f"📍 API URL: {base_url}")
            print(f"🍪 Cookie长度: {len(cookie_text)} 字符")

            # 检查基本配置
            config_issues = []
            if not base_url:
                config_issues.append("❌ API URL为空")
            elif not base_url.startswith('http'):
                config_issues.append("❌ API URL格式不正确")

            if not cookie_text:
                config_issues.append("❌ Cookie为空")
            elif '_session=' not in cookie_text:
                config_issues.append("⚠️ Cookie中缺少 _session 字段")
            elif 'ajs_user_id=' not in cookie_text:
                config_issues.append("⚠️ Cookie中缺少 ajs_user_id 字段")

            if config_issues:
                issue_text = "\n".join(config_issues)
                print(f"配置问题:\n{issue_text}")
                self.update_config_status("❌ 配置有问题", StyleManager.WARNING_COLOR)
                CustomMessageBox.show_warning(self, "配置检查", f"⚠️ 发现配置问题：\n\n{issue_text}\n\n请修正后重试。")
                return

            # 创建临时API客户端
            temp_api = APIClient(temp_config)

            print("🚀 开始API连接测试...")
            self.update_config_status("🔄 正在测试连接...", StyleManager.PRIMARY_COLOR)

            # 测试连接
            success, result = temp_api.get_team_data()

            print("="*60)
            print("🔧 配置连接测试结果")
            print("="*60)

            if success:
                print("✅ 连接测试成功！")
                self.update_config_status("✅ 连接测试成功", StyleManager.SUCCESS_COLOR)

                # 显示团队数据摘要
                from PyQt6.QtWidgets import QMessageBox
                if isinstance(result, dict):
                    team_info = []
                    if 'members' in result:
                        team_info.append(f"团队成员: {len(result['members'])}人")
                    if 'pendingInvitations' in result:
                        team_info.append(f"待处理邀请: {len(result['pendingInvitations'])}个")
                    if 'teamName' in result:
                        team_info.append(f"团队名称: {result['teamName']}")

                    info_text = "\n".join(team_info) if team_info else "成功获取团队数据"
                    CustomMessageBox.show_success(self, "连接测试", f"✅ API连接测试成功！\n\n{info_text}\n\n配置正确，可以正常使用。")
                else:
                    CustomMessageBox.show_success(self, "连接测试", "✅ API连接测试成功！\n配置正确，可以正常使用。")
            else:
                print(f"❌ 连接测试失败: {result}")
                self.update_config_status("❌ 连接测试失败", StyleManager.DANGER_COLOR)

                # 分析错误原因
                error_analysis = self.analyze_connection_error(result)
                CustomMessageBox.show_error(self, "连接测试", f"❌ API连接测试失败！\n\n错误信息：{result}\n\n{error_analysis}")

        except Exception as e:
            print(f"❌ 连接测试异常: {str(e)}")
            self.update_config_status("❌ 测试异常", StyleManager.DANGER_COLOR)
            CustomMessageBox.show_error(self, "连接测试", f"❌ 连接测试异常！\n\n错误信息：{str(e)}")

    def analyze_connection_error(self, error_message: str) -> str:
        """分析连接错误并提供解决建议"""
        error_lower = error_message.lower()

        if "401" in error_message or "unauthorized" in error_lower:
            return ("🔍 错误分析：认证失败\n"
                   "💡 解决建议：\n"
                   "1. 检查Cookie是否过期\n"
                   "2. 重新从浏览器复制最新的Cookie\n"
                   "3. 确保Cookie包含完整的认证信息")

        elif "403" in error_message or "forbidden" in error_lower:
            return ("🔍 错误分析：访问被拒绝\n"
                   "💡 解决建议：\n"
                   "1. 检查账号权限\n"
                   "2. 确认Cookie对应的账号有团队管理权限")

        elif "404" in error_message or "not found" in error_lower:
            return ("🔍 错误分析：API端点不存在\n"
                   "💡 解决建议：\n"
                   "1. 检查API URL是否正确\n"
                   "2. 确认API版本是否匹配")

        elif "timeout" in error_lower or "连接超时" in error_message:
            return ("🔍 错误分析：网络连接超时\n"
                   "💡 解决建议：\n"
                   "1. 检查网络连接\n"
                   "2. 尝试使用VPN或代理")

        elif "ssl" in error_lower or "certificate" in error_lower:
            return ("🔍 错误分析：SSL证书问题\n"
                   "💡 解决建议：\n"
                   "1. 检查系统时间是否正确\n"
                   "2. 更新系统证书")

        elif "json" in error_lower:
            return ("🔍 错误分析：响应格式错误\n"
                   "💡 解决建议：\n"
                   "1. 可能返回了HTML错误页面\n"
                   "2. 检查Cookie是否正确")

        else:
            return ("🔍 错误分析：未知错误\n"
                   "💡 解决建议：\n"
                   "1. 检查网络连接\n"
                   "2. 重新获取Cookie\n"
                   "3. 联系技术支持")

    def validate_cookie(self):
        """验证Cookie格式"""
        cookie_text = self.cookie_edit.toPlainText().strip()

        if not cookie_text:
            self.cookie_status_label.setText("Cookie状态: 未输入")
            self.cookie_status_label.setStyleSheet("""
                QLabel {
                    padding: 8px;
                    border-radius: 4px;
                    background: #f8f9fa;
                    border: 1px solid #dee2e6;
                    color: #6c757d;
                    font-size: 12px;
                }
            """)
            return

        # 检查关键字段
        required_fields = ['_session=', 'ajs_user_id=']
        missing_fields = []

        for field in required_fields:
            if field not in cookie_text:
                missing_fields.append(field.replace('=', ''))

        if missing_fields:
            self.cookie_status_label.setText(f"Cookie状态: 缺少关键字段 {', '.join(missing_fields)}")
            self.cookie_status_label.setStyleSheet("""
                QLabel {
                    padding: 8px;
                    border-radius: 4px;
                    background: #fff3cd;
                    border: 1px solid #ffeaa7;
                    color: #856404;
                    font-size: 12px;
                }
            """)
        else:
            self.cookie_status_label.setText(f"Cookie状态: 格式正确 ({len(cookie_text)} 字符)")
            self.cookie_status_label.setStyleSheet("""
                QLabel {
                    padding: 8px;
                    border-radius: 4px;
                    background: #d4edda;
                    border: 1px solid #c3e6cb;
                    color: #155724;
                    font-size: 12px;
                }
            """)

    def validate_cookie_detailed(self):
        """详细验证Cookie"""
        cookie_text = self.cookie_edit.toPlainText().strip()

        if not cookie_text:
            CustomMessageBox.show_warning(self, "Cookie验证", "请先输入Cookie内容")
            return

        # 解析Cookie
        cookie_pairs = []
        for pair in cookie_text.split(';'):
            pair = pair.strip()
            if '=' in pair:
                key, value = pair.split('=', 1)
                cookie_pairs.append((key.strip(), value.strip()))

        # 检查关键字段
        analysis = []
        analysis.append(f"📊 Cookie分析报告")
        analysis.append(f"总长度: {len(cookie_text)} 字符")
        analysis.append(f"字段数量: {len(cookie_pairs)} 个")
        analysis.append("")

        # 检查必需字段
        required_checks = {
            '_session': '会话认证令牌',
            'ajs_user_id': '用户ID',
            '_ga': 'Google Analytics',
            'ph_phc': 'PostHog Analytics'
        }

        analysis.append("🔍 关键字段检查:")
        for field, description in required_checks.items():
            found = any(key.startswith(field) for key, _ in cookie_pairs)
            status = "✅" if found else "❌"
            analysis.append(f"{status} {field}: {description}")

        analysis.append("")
        analysis.append("📋 所有字段:")
        for key, value in cookie_pairs[:10]:  # 只显示前10个
            short_value = value[:30] + "..." if len(value) > 30 else value
            analysis.append(f"• {key}: {short_value}")

        if len(cookie_pairs) > 10:
            analysis.append(f"... 还有 {len(cookie_pairs) - 10} 个字段")

        CustomMessageBox.show_info(self, "Cookie详细验证", "\n".join(analysis))

    def show_cookie_help(self):
        """显示Cookie获取帮助"""
        help_text = """
🍪 如何获取Cookie认证信息

📋 步骤说明：
1. 打开浏览器，访问 https://app.augmentcode.com
2. 登录您的账号
3. 按F12打开开发者工具
4. 切换到"Network"(网络)标签页
5. 刷新页面或进行任何操作
6. 找到任意一个请求，点击查看
7. 在请求头中找到"Cookie"字段
8. 复制完整的Cookie值

🔍 关键字段说明：
• _session: 会话认证令牌（最重要）
• ajs_user_id: 用户唯一标识
• _ga: Google Analytics追踪
• ph_phc: PostHog分析数据

⚠️ 注意事项：
• Cookie包含敏感信息，请勿泄露
• Cookie有时效性，过期需重新获取
• 确保复制完整，不要遗漏任何字符
• 如果登录状态改变，需要更新Cookie

💡 常见问题：
• 401错误：Cookie过期或无效
• 403错误：账号权限不足
• 空响应：Cookie格式错误

🔧 快速检查：
使用"验证Cookie"按钮检查格式是否正确
使用"测试连接"按钮验证是否能正常访问API
        """

        CustomMessageBox.show_info(self, "Cookie获取帮助", help_text)

    def update_config_status(self, message, color):
        """更新配置状态显示"""
        if hasattr(self, 'config_status_label'):
            self.config_status_label.setText(f"配置状态: {message}")
            # 根据消息类型设置颜色
            if "成功" in message or "已保存" in message or "已重置" in message:
                color_to_use = StyleManager.SUCCESS_COLOR
            elif "失败" in message or "错误" in message:
                color_to_use = StyleManager.DANGER_COLOR
            elif "测试" in message:
                color_to_use = StyleManager.PRIMARY_COLOR
            else:
                color_to_use = color
                
            self.config_status_label.setStyleSheet(f"""
                QLabel {{
                    padding: 10px;
                    border-radius: 6px;
                    background: {color_to_use}20;
                    border: 1px solid {color_to_use};
                    color: {color_to_use};
                    font-weight: bold;
                }}
            """)

    def browse_config_file(self):
        """浏览配置文件"""
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择配置文件", "", "JSON文件 (*.json);;所有文件 (*)"
        )
        if file_path:
            self.config_path_display.setText(file_path)

    def export_config(self):
        """导出配置"""
        from PyQt6.QtWidgets import QFileDialog
        from datetime import datetime

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        default_name = f"team_manager_config_{timestamp}.json"

        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出配置", default_name, "JSON文件 (*.json);;所有文件 (*)"
        )
        if file_path:
            try:
                import json
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.config.config, f, indent=2, ensure_ascii=False)
                print(f"✅ 配置已导出到: {file_path}")
                self.update_config_status("✅ 配置导出成功", StyleManager.SUCCESS_COLOR)
            except Exception as e:
                print(f"❌ 导出配置失败: {str(e)}")
                self.update_config_status(f"❌ 导出失败: {str(e)}", StyleManager.DANGER_COLOR)

    def import_config(self):
        """导入配置"""
        from PyQt6.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入配置", "", "JSON文件 (*.json);;所有文件 (*)"
        )
        if file_path:
            try:
                import json
                with open(file_path, 'r', encoding='utf-8') as f:
                    imported_config = json.load(f)

                # 确认导入
                if CustomConfirmDialog.ask_confirmation(
                    self, "确认导入",
                    "导入配置将覆盖当前设置，是否继续？"
                ):
                    self.config.config.update(imported_config)
                    self.config.save_config()
                    print(f"✅ 配置已从 {file_path} 导入")
                    self.update_config_status("✅ 配置导入成功", StyleManager.SUCCESS_COLOR)

            except Exception as e:
                print(f"❌ 导入配置失败: {str(e)}")
                self.update_config_status(f"❌ 导入失败: {str(e)}", StyleManager.DANGER_COLOR)

    def clear_cache(self):
        """清理缓存"""
        try:
            # 这里可以添加清理缓存的逻辑
            print("🧹 缓存已清理")
            self.update_config_status("✅ 缓存清理完成", StyleManager.SUCCESS_COLOR)
        except Exception as e:
            print(f"❌ 清理缓存失败: {str(e)}")
            self.update_config_status(f"❌ 清理失败: {str(e)}", StyleManager.DANGER_COLOR)


class TeamManagerMainWindow(QMainWindow):
    """Main window with completely redesigned UI"""

    def __init__(self):
        super().__init__()
        self.config = Config()
        self.api_client = APIClient(self.config)
        self.team_data = None
        self.worker_thread = None
        # 记录连接状态，便于全局控制
        self.is_connected = False

        # 定义一个主要的连接状态显示组件，其他地方引用这个
        self.connection_status = None
        
        self.setWindowTitle("团队管理工具")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 700)
        
        # 创建系统托盘
        self.setup_tray_icon()

        # 应用配置
        app = QApplication.instance()
        app.setStyleSheet(StyleManager.get_app_style())
        
        # 应用字体大小
        font_size = self.config.get('ui.font_size', 10)
        font = app.font()
        font.setPointSize(font_size)
        app.setFont(font)
        
        # 应用透明度
        opacity = self.config.get('ui.opacity', 100) / 100
        self.setWindowOpacity(opacity)

        # 启动时最小化
        if self.config.get('ui.start_minimized', False):
            self.showMinimized()

        # Create the overlay for loading states
        self.loading_overlay = QWidget(self)
        self.loading_overlay.setGeometry(self.rect())
        self.loading_overlay.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0.4);
            }
        """)
        self.loading_overlay.hide()
        
        # Loading container with modern design
        self.loading_container = QWidget(self.loading_overlay)
        self.loading_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)
        self.loading_container.setFixedSize(280, 160)
        
        # Loading layout
        loading_layout = QVBoxLayout(self.loading_container)
        loading_layout.setContentsMargins(20, 20, 20, 20)
        loading_layout.setSpacing(15)
        
        # 加载文本
        self.loading_label = QLabel("正在加载...")
        self.loading_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #4361ee;
        """)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 加载进度条
        self.loading_progress = QProgressBar()
        self.loading_progress.setRange(0, 0)  # 不确定状态的进度条
        self.loading_progress.setFixedHeight(6)
        
        # 加载状态文本
        self.loading_status = QLabel("正在连接服务器...")
        self.loading_status.setStyleSheet("""
            font-size: 13px;
            color: #64748b;
        """)
        self.loading_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add to loading layout
        loading_layout.addWidget(self.loading_label)
        loading_layout.addWidget(self.loading_progress)
        loading_layout.addWidget(self.loading_status)
        loading_layout.addStretch()
        
        # Apply shadow effect
        StyleManager.apply_shadow_effect(self.loading_container)

        # Initialize the UI components
        self.init_ui()
        self.init_menu()
        self.init_status_bar()

        # Set up refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.auto_refresh_data)
        self.update_refresh_timer()
        
    def setup_tray_icon(self):
        """设置系统托盘图标"""
        # 创建系统托盘
        self.tray_icon = QSystemTrayIcon(self)
        
        # 设置图标 - 如果没有图标文件，使用默认或空图标
        try:
            icon = QIcon("team_manager_icon.png")  # 可以替换为实际的图标路径
            if icon.isNull():
                # 如果图标加载失败，使用默认图标
                icon = QIcon.fromTheme("applications-system")
            self.tray_icon.setIcon(icon)
        except Exception as e:
            print(f"无法加载托盘图标: {e}")
        
        # 创建托盘菜单
        tray_menu = QMenu()
        
        # 添加菜单项
        show_action = QAction("显示", self)
        show_action.triggered.connect(self.show_from_tray)
        tray_menu.addAction(show_action)
        
        hide_action = QAction("隐藏", self)
        hide_action.triggered.connect(self.hide)
        tray_menu.addAction(hide_action)
        
        tray_menu.addSeparator()
        
        refresh_action = QAction("刷新数据", self)
        refresh_action.triggered.connect(self.refresh_team_data)
        tray_menu.addAction(refresh_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_from_tray)
        tray_menu.addAction(quit_action)
        
        # 设置托盘菜单
        self.tray_icon.setContextMenu(tray_menu)
        
        # 连接托盘图标的点击信号
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        # 显示托盘图标
        self.tray_icon.show()
        
    def tray_icon_activated(self, reason):
        """处理托盘图标激活事件"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # 单击图标切换显示/隐藏状态
            if self.isHidden():
                self.show_from_tray()
            else:
                self.hide()
    
    def show_from_tray(self):
        """从托盘显示窗口"""
        self.show()
        self.activateWindow()  # 将窗口带到前台
        self.log_info("系统托盘", "从系统托盘恢复窗口")
        
    def quit_from_tray(self):
        """从托盘退出程序"""
        self.log_info("系统托盘", "通过系统托盘退出应用")
        QApplication.quit()
        
    def closeEvent(self, event):
        """关闭事件处理"""
        if self.config.get('features.auto_save', True):
            self.config.save_config()

        if self.worker_thread and self.worker_thread.isRunning():
            self.log_warning("退出确认", "有操作正在进行中，强制退出可能导致数据丢失")
            self.worker_thread.terminate()
            self.worker_thread.wait()

        # 检查是否应该关闭到系统托盘
        if self.config.get('ui.close_to_tray', False) and self.tray_icon.isVisible():
            self.log_info("应用最小化", "已最小化到系统托盘")
            self.hide()
            event.ignore()
        else:
            self.log_info("应用退出", "团队管理工具正在关闭...")
            event.accept()

    def resizeEvent(self, event):
        """Handle window resize event"""
        super().resizeEvent(event)
        self.loading_overlay.setGeometry(self.rect())
        # Center the loading container
        self.loading_container.move(
            (self.width() - self.loading_container.width()) // 2,
            (self.height() - self.loading_container.height()) // 2
        )
        
    def show_loading(self, message="正在加载数据...", status=""):
        """显示加载覆盖层及消息"""
        self.loading_label.setText(message)
        if status:
            self.loading_status.setText(status)
        self.loading_overlay.show()
        self.loading_container.move(
            (self.width() - self.loading_container.width()) // 2,
            (self.height() - self.loading_container.height()) // 2
        )
        
    def hide_loading(self):
        """隐藏加载覆盖层"""
        self.loading_overlay.hide()

    def init_ui(self):
        """Initialize the new user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 头部区域
        header = self.create_header_widget()
        main_layout.addWidget(header)

        # 标签页容器
        self.tab_widget = QTabWidget()
        self.tab_widget.setMinimumHeight(500)

        # Create tabs
        invite_tab = self.create_invite_tab()
        self.tab_widget.addTab(invite_tab, "邀请成员")

        manage_tab = self.create_manage_tab()
        self.tab_widget.addTab(manage_tab, "团队管理")

        batch_tab = self.create_batch_tab()
        self.tab_widget.addTab(batch_tab, "批量操作")

        data_tab = self.create_data_tab()
        self.tab_widget.addTab(data_tab, "数据视图")

        main_layout.addWidget(self.tab_widget, 1)

        # Log panel
        log_panel = self.create_log_widget()
        main_layout.addWidget(log_panel)

        central_widget.setLayout(main_layout)
        
        # 应用视觉效果
        self.apply_visual_effects()

    def create_header_widget(self):
        """Create the header widget with a new design"""
        header = QFrame()
        header.setFixedHeight(100)
        header.setObjectName("header")
        header.setStyleSheet(f"""
            #header {{
                background: {StyleManager.PRIMARY_COLOR};
                border-radius: 8px;
            }}
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 12, 20, 12)
        
        # Left side - Logo and app name
        left_container = QWidget()
        left_layout = QHBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)
        
        # 应用图标
        logo_label = QLabel("🚀")
        logo_label.setStyleSheet("""
            font-size: 32px;
            color: white;
        """)
        
        # 应用名称
        app_name = QLabel("团队管理工具")
        app_name.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
        """)
        
        # 添加居中标题标签
        center_title = QLabel("团队管理工具")
        center_title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
        """)
        center_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        left_layout.addWidget(logo_label)
        left_layout.addWidget(app_name)
        
        # Right side - Status and actions
        right_container = QWidget()
        right_layout = QHBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(20)
        
        # 连接状态 - 统一样式
        self.connection_status = QLabel("🔴 未连接") 
        # 根据当前连接状态设置样式
        if self.is_connected:
            self.connection_status.setText("🟢 已连接")
            self.connection_status.setStyleSheet("""
                QLabel {
                    background: rgba(238, 219, 205, 0.8);
                    border: 2px solid #43e97b;
                    border-radius: 20px;
                    padding: 12px 25px;
                    font-weight: 600;
                    font-size: 16px;
                    color: #22c55e;
                }
            """)
        else:
            self.connection_status.setStyleSheet("""
                background: rgba(93, 102, 217, 0.8);
                border-radius: 20px;
                padding: 12px 25px;
                color: white;
                font-size: 16px;
                font-weight: 600;
            """)

        # 刷新按钮
        self.refresh_button = QPushButton("🔄 刷新数据")
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.25);
                border: none;
                border-radius: 20px;
                color: white;
                padding: 12px 25px;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.35);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.2);
            }
        """)
        self.refresh_button.clicked.connect(self.refresh_team_data)
        
        right_layout.addWidget(self.connection_status)
        right_layout.addWidget(self.refresh_button)
        
        # Add containers to main layout
        layout.addWidget(left_container, 1)
        layout.addWidget(center_title, 2)
        layout.addWidget(right_container)
        
        StyleManager.apply_shadow_effect(header)
        return header

    def create_log_widget(self):
        """创建现代日志组件"""
        log_panel = StyleManager.create_card(title="系统日志", icon="📋")
        
        # 创建内容组件
        content_widget = QWidget()
        log_layout = QVBoxLayout(content_widget)
        log_layout.setContentsMargins(0, 0, 0, 0)
        log_layout.setSpacing(10)
        
        # 日志控制区
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        level_label = QLabel("日志级别:")
        
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["全部", "信息", "成功", "警告", "错误"])
        self.log_level_combo.currentTextChanged.connect(self.filter_logs)
        
        clear_btn = QPushButton("清空")
        clear_btn.clicked.connect(self.clear_logs)
        
        export_btn = QPushButton("导出")
        export_btn.clicked.connect(self.export_logs)
        
        self.auto_scroll_checkbox = QCheckBox("自动滚动")
        self.auto_scroll_checkbox.setChecked(True)
        
        controls_layout.addWidget(level_label)
        controls_layout.addWidget(self.log_level_combo)
        controls_layout.addWidget(clear_btn)
        controls_layout.addWidget(export_btn)
        controls_layout.addStretch()
        controls_layout.addWidget(self.auto_scroll_checkbox)
        
        # Log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setMaximumHeight(150)
        self.log_display.setStyleSheet("""
            QTextEdit {
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        
        log_layout.addLayout(controls_layout)
        log_layout.addWidget(self.log_display)
        
        # Initialize log storage
        self.log_entries = []
        
        # Add content widget to card
        log_panel.layout().addWidget(content_widget)
        
        # 初始化欢迎消息
        QTimer.singleShot(100, lambda: self.log_info("系统", "团队管理工具已启动。"))
        
        return log_panel

    # ==================== 日志管理方法 ====================

    def log_info(self, title, message):
        """记录信息日志"""
        self._add_log_entry("信息", title, message, "#17a2b8")

    def log_success(self, title, message):
        """记录成功日志"""
        self._add_log_entry("成功", title, message, "#28a745")

    def log_warning(self, title, message):
        """记录警告日志"""
        self._add_log_entry("警告", title, message, "#ffc107")

    def log_error(self, title, message):
        """记录错误日志"""
        self._add_log_entry("错误", title, message, "#dc3545")

    def _add_log_entry(self, level, title, message, color):
        """添加日志条目"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%H:%M:%S')

        # 创建日志条目
        log_entry = {
            'timestamp': timestamp,
            'level': level,
            'title': title,
            'message': message,
            'color': color,
            'full_timestamp': datetime.now()
        }

        # 添加到日志列表
        self.log_entries.append(log_entry)

        # 限制日志条目数量（保留最近1000条）
        if len(self.log_entries) > 1000:
            self.log_entries = self.log_entries[-1000:]

        # 更新显示
        self._update_log_display()

        # 同时输出到控制台
        print(f"[{timestamp}] {level}: {title} - {message}")

    def _update_log_display(self):
        """更新日志显示 - 现代化版2.0"""
        if not hasattr(self, 'log_display'):
            return

        # 获取当前过滤级别
        filter_level = self.log_level_combo.currentText() if hasattr(self, 'log_level_combo') else "全部"

        # 过滤日志条目
        filtered_entries = []
        for entry in self.log_entries:
            if filter_level == "全部" or entry['level'] == filter_level:
                filtered_entries.append(entry)

        # 构建更现代的HTML内容
        html_content = """
        <style>
            .log-container {
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                padding: 0;
                margin: 0;
            }
            .log-entry {
                margin-bottom: 8px;
                padding: 8px 12px;
                border-radius: 10px;
                background: rgba(250, 250, 250, 0.9);
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                transition: transform 0.2s;
            }
            .log-entry:hover {
                transform: translateY(-2px);
                box-shadow: 0 3px 5px rgba(0,0,0,0.15);
            }
            .log-header {
                display: flex;
                align-items: center;
                margin-bottom: 4px;
            }
            .log-time {
                color: #64748b;
                font-size: 11px;
                margin-right: 8px;
                padding: 2px 6px;
                background: rgba(0,0,0,0.05);
                border-radius: 10px;
            }
            .log-level {
                font-weight: bold;
                padding: 2px 8px;
                border-radius: 10px;
                margin-right: 8px;
                font-size: 12px;
            }
            .log-level-info {
                background: #3b82f6;
                color: white;
            }
            .log-level-success {
                background: #10b981;
                color: white;
            }
            .log-level-warning {
                background: #f59e0b;
                color: white;
            }
            .log-level-error {
                background: #ef4444;
                color: white;
            }
            .log-title {
                color: #1e293b;
                font-weight: 600;
                font-size: 13px;
                flex-grow: 1;
            }
            .log-message {
                color: #475569;
                margin-left: 20px;
                line-height: 1.4;
                font-size: 12px;
                white-space: pre-wrap;
            }
        </style>
        <div class="log-container">
        """
        
        # 日志条目
        for entry in filtered_entries[-100:]:  # 只显示最近100条
            # 根据级别选择不同的样式
            level_class = "log-level-info"
            if entry['level'] == "成功":
                level_class = "log-level-success"
            elif entry['level'] == "警告":
                level_class = "log-level-warning"
            elif entry['level'] == "错误":
                level_class = "log-level-error"
                
            html_content += f"""
            <div class="log-entry">
                <div class="log-header">
                    <span class="log-time">{entry['timestamp']}</span>
                    <span class="log-level {level_class}">{entry['level']}</span>
                    <span class="log-title">{entry['title']}</span>
                </div>
                <div class="log-message">{entry['message']}</div>
            </div>
            """
            
        html_content += "</div>"

        # 更新显示
        self.log_display.setHtml(html_content)

        # 自动滚动到底部
        if hasattr(self, 'auto_scroll_checkbox') and self.auto_scroll_checkbox.isChecked():
            scrollbar = self.log_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def filter_logs(self):
        """过滤日志显示"""
        self._update_log_display()

    def clear_logs(self):
        """清空日志"""
        self.log_entries.clear()
        self.log_display.clear()
        self.log_info("系统操作", "日志已清空")

    def export_logs(self):
        """导出日志"""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"team_manager_logs_{timestamp}.txt"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"团队管理工具日志导出\n")
                f.write(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")

                for entry in self.log_entries:
                    f.write(f"[{entry['full_timestamp'].strftime('%Y-%m-%d %H:%M:%S')}] ")
                    f.write(f"{entry['level']}: {entry['title']}\n")
                    f.write(f"  {entry['message']}\n\n")

            self.log_success("日志导出", f"日志已导出到文件: {filename}")

        except Exception as e:
            self.log_error("日志导出失败", f"导出日志时发生错误: {str(e)}")

    def create_modern_title_widget(self):
        """创建全新现代化标题区域 3.0"""
        title_widget = QWidget()
        title_widget.setFixedHeight(180)
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(40, 30, 40, 30)

        # 左侧图标和标题区域
        left_widget = QWidget()
        left_layout = QHBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(30)

        # 全新设计的图标容器
        icon_container = QWidget()
        icon_container.setFixedSize(120, 120)
        icon_container.setStyleSheet("""
            QWidget {
                background: qradialgradient(cx:0.5, cy:0.5, radius: 1, fx:0.5, fy:0.5, 
                                         stop:0 rgba(255, 255, 255, 0.4), 
                                         stop:0.5 rgba(255, 255, 255, 0.2),
                                         stop:1 rgba(255, 255, 255, 0.1));
                border-radius: 60px;
                border: 3px solid rgba(255, 255, 255, 0.5);
            }
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        # 增强版图标
        icon_label = QLabel("🚀")
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 60px;
                color: white;
                background: transparent;
            }
        """)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon_label)
        
        # 图标底部添加闪光效果
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(30)
        glow_effect.setColor(QColor(255, 255, 255, 200))
        glow_effect.setOffset(0, 0)
        icon_label.setGraphicsEffect(glow_effect)

        # 全新标题和副标题设计
        text_widget = QWidget()
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(15)

        # 增强主标题
        title_label = QLabel("团队管理工具")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 44px;
                font-weight: 900;
                color: white;
                background: transparent;
                letter-spacing: 2px;
            }
        """)
        
        # 标题添加文字阴影
        title_shadow = QGraphicsDropShadowEffect()
        title_shadow.setBlurRadius(20)
        title_shadow.setColor(QColor(0, 0, 0, 100))
        title_shadow.setOffset(2, 2)
        title_label.setGraphicsEffect(title_shadow)

        # 增强副标题
        subtitle_label = QLabel("🌟 现代化团队协作管理平台 · 高效 · 智能 · 美观")
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 600;
                color: rgba(255, 255, 255, 0.95);
                background: transparent;
                letter-spacing: 1px;
            }
        """)

        text_layout.addWidget(title_label)
        text_layout.addWidget(subtitle_label)
        text_layout.addStretch()
        text_widget.setLayout(text_layout)

        left_layout.addWidget(icon_container)
        left_layout.addWidget(text_widget)
        left_widget.setLayout(left_layout)

        # 全新右侧状态和版本信息
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(15)

        # 增强版本标签
        version_label = QLabel("v3.0 Pro")
        version_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 800;
                color: white;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                          stop: 0 rgba(255, 255, 255, 0.3),
                                          stop: 1 rgba(255, 255, 255, 0.2));
                border-radius: 22px;
                padding: 14px 24px;
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
        """)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        StyleManager.apply_shadow_effect(version_label, blur_radius=15, offset=(0, 4))

        # 增强在线状态
        status_label = QLabel("✨ 系统就绪")
        status_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 700;
                color: white;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                          stop: 0 rgba(34, 197, 94, 0.4),
                                          stop: 1 rgba(16, 185, 129, 0.4));
                border-radius: 22px;
                padding: 14px 24px;
                border: 2px solid rgba(34, 197, 94, 0.5);
            }
        """)
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        StyleManager.apply_shadow_effect(status_label, blur_radius=15, offset=(0, 4))

        # 创建快速刷新面板（对应图片中红框标记的区域）
        refresh_panel = QWidget()
        refresh_panel.setFixedSize(150, 170)  # 设置合适的尺寸
        refresh_panel.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 rgba(255, 255, 255, 0.25), 
                                          stop: 1 rgba(255, 255, 255, 0.15));
                border-radius: 20px;
                border: 2px solid rgba(255, 255, 255, 0.4);
            }
        """)
        refresh_layout = QVBoxLayout(refresh_panel)
        refresh_layout.setContentsMargins(15, 15, 15, 15)
        refresh_layout.setSpacing(8)
        
        # 顶部半透明条块
        top_bar = QWidget()
        top_bar.setFixedHeight(20)
        top_bar.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.6);
                border-radius: 5px;
            }
        """)
        
        # 中间绿色进度条（第一个）
        progress_bar1 = QWidget()
        progress_bar1.setFixedHeight(20)
        progress_bar1.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                          stop: 0 rgba(52, 211, 153, 0.9), 
                                          stop: 1 rgba(16, 185, 129, 0.8));
                border-radius: 5px;
            }
        """)
        
        # 中间绿色进度条（第二个）
        progress_bar2 = QWidget()
        progress_bar2.setFixedHeight(20)
        progress_bar2.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                          stop: 0 rgba(59, 130, 246, 0.9), 
                                          stop: 1 rgba(37, 99, 235, 0.8));
                border-radius: 5px;
            }
        """)
        
        # 底部刷新按钮
        refresh_btn = QPushButton("⟳ 快速刷新")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                          stop: 0 rgba(16, 185, 129, 0.9), 
                                          stop: 1 rgba(5, 150, 105, 0.9));
                color: white;
                border: none;
                border-radius: 15px;
                padding: 10px;
                font-weight: 700;
                font-size: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                          stop: 0 rgba(5, 150, 105, 0.9), 
                                          stop: 1 rgba(16, 185, 129, 0.9));
            }
            QPushButton:pressed {
                background: rgba(5, 150, 105, 1);
            }
        """)
        refresh_btn.clicked.connect(self.refresh_team_data)
        
        # 添加所有元素到刷新面板
        refresh_layout.addWidget(top_bar)
        refresh_layout.addWidget(progress_bar1)
        refresh_layout.addWidget(progress_bar2)
        refresh_layout.addStretch()
        refresh_layout.addWidget(refresh_btn)
        
        # 添加阴影效果
        StyleManager.apply_shadow_effect(refresh_panel, blur_radius=20, offset=(0, 5))

        right_layout.addWidget(version_label)
        right_layout.addWidget(status_label)
        right_layout.addStretch()
        right_widget.setLayout(right_layout)

        # 主布局
        title_layout.addWidget(left_widget)
        title_layout.addStretch()
        title_layout.addWidget(refresh_panel)  # 添加刷新面板
        title_layout.addWidget(right_widget)

        title_widget.setLayout(title_layout)

        # 增强背景设计 - 添加更高级的玻璃拟态效果
        title_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 rgba(255, 255, 255, 0.22),
                                          stop: 0.3 rgba(255, 255, 255, 0.16),
                                          stop: 0.7 rgba(255, 255, 255, 0.12),
                                          stop: 1 rgba(255, 255, 255, 0.18));
                border-radius: 35px;
                border: 3px solid rgba(255, 255, 255, 0.4);
            }
        """)

        # 增强阴影效果
        StyleManager.apply_shadow_effect(title_widget, blur_radius=25, offset=(0, 10))

        return title_widget

    def apply_visual_effects(self):
        """应用视觉效果"""
        # 为标签页添加阴影
        StyleManager.apply_shadow_effect(self.tab_widget, blur_radius=15, offset=(0, 5))

    def init_menu(self):
        """初始化菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件")

        # 导入配置
        import_action = QAction("导入配置", self)
        import_action.triggered.connect(self.import_config)
        file_menu.addAction(import_action)

        # 导出配置
        export_action = QAction("导出配置", self)
        export_action.triggered.connect(self.export_config)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        # 退出
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 工具菜单
        tools_menu = menubar.addMenu("工具")

        # 配置设置
        config_action = QAction("配置设置", self)
        config_action.triggered.connect(self.open_config_dialog)
        tools_menu.addAction(config_action)

        # 刷新数据
        refresh_action = QAction("刷新数据", self)
        refresh_action.triggered.connect(self.refresh_team_data)
        tools_menu.addAction(refresh_action)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助")

        # 关于
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def init_status_bar(self):
        """初始化状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # 添加状态标签
        self.status_label = QLabel("就绪")
        self.status_bar.addWidget(self.status_label)

        # 添加进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)

        # 添加连接状态 - 根据当前连接状态设置初始文本
        self.connection_label = QLabel("🔴 未连接")
        self.connection_label.setStyleSheet(f"color: {StyleManager.DANGER_COLOR}; font-weight: 700; padding-right: 10px;")
        self.status_bar.addPermanentWidget(self.connection_label)

    def create_invite_tab(self) -> QWidget:
        """创建邀请成员标签页（新UI设计）"""
        # 主容器
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # 信息卡片
        info_card = StyleManager.create_card(
            title="邀请团队成员",
            icon="✉️"
        )
        info_content = QLabel(
            "每行输入一个邮箱地址。"
            "系统将自动验证格式并发送邀请。"
        )
        info_content.setWordWrap(True)
        info_content.setStyleSheet("color: #64748b; line-height: 1.4;")
        info_card.layout().addWidget(info_content)
        layout.addWidget(info_card)

        # 邮箱输入卡片
        input_card = StyleManager.create_card(title="邮箱地址", icon="📧")
        
        # 邮箱输入字段
        self.email_input = QTextEdit()
        self.email_input.setPlaceholderText("example1@gmail.com\nexample2@gmail.com\nexample3@gmail.com")
        self.email_input.setMinimumHeight(150)
        self.email_input.textChanged.connect(self.validate_emails_realtime)
        
        # 统计行
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)
        
        # 使用新设计的统计卡片
        self.total_emails_card = StyleManager.create_stat_card("📊", "总邮箱数", "0", StyleManager.PRIMARY_COLOR)
        self.valid_emails_card = StyleManager.create_stat_card("✅", "有效邮箱", "0", StyleManager.SUCCESS_COLOR)
        self.invalid_emails_card = StyleManager.create_stat_card("❌", "无效邮箱", "0", StyleManager.DANGER_COLOR)
        
        stats_layout.addWidget(self.total_emails_card)
        stats_layout.addWidget(self.valid_emails_card)
        stats_layout.addWidget(self.invalid_emails_card)
        stats_layout.addStretch()
        
        # 进度容器
        progress_container = QWidget()
        progress_layout = QVBoxLayout(progress_container)
        progress_layout.setContentsMargins(0, 10, 0, 0)
        progress_layout.setSpacing(5)
        
        progress_label = QLabel("验证进度:")
        
        self.validation_progress = QProgressBar()
        self.validation_progress.setValue(0)
        self.validation_progress.setMaximum(100)
        
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.validation_progress)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.invite_btn = StyleManager.create_button("发送邀请", "success", "✉️")
        self.invite_btn.setMinimumWidth(150)
        self.invite_btn.clicked.connect(self.invite_members)
        self.invite_btn.setEnabled(False)
        
        self.clear_btn = StyleManager.create_button("清空输入", "danger", "🗑️")
        self.clear_btn.setMinimumWidth(150) 
        self.clear_btn.clicked.connect(self.clear_email_input)
        
        self.paste_btn = StyleManager.create_button("从剪贴板粘贴", "primary", "📋")
        self.paste_btn.setMinimumWidth(150)
        self.paste_btn.clicked.connect(self.paste_clipboard)
        
        button_layout.addWidget(self.invite_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.paste_btn)
        button_layout.addStretch()
        
        # Add all elements to input card
        input_content = QWidget()
        input_content_layout = QVBoxLayout(input_content)
        input_content_layout.setContentsMargins(0, 0, 0, 0)
        input_content_layout.setSpacing(15)
        
        input_content_layout.addWidget(self.email_input)
        input_content_layout.addLayout(stats_layout)
        input_content_layout.addWidget(progress_container)
        input_content_layout.addLayout(button_layout)
        
        input_card.layout().addWidget(input_content)
        layout.addWidget(input_card)
        
        # 历史记录卡片
        history_card = StyleManager.create_card(title="邀请历史", icon="📋")
        
        self.invite_history = QTextEdit()
        self.invite_history.setReadOnly(True)
        self.invite_history.setMinimumHeight(120)
        self.invite_history.setStyleSheet("""
            QTextEdit {
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        
        history_card.layout().addWidget(self.invite_history)
        layout.addWidget(history_card)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container)
        
        # Final container 
        final_container = QWidget()
        final_layout = QVBoxLayout(final_container)
        final_layout.setContentsMargins(0, 0, 0, 0)
        final_layout.addWidget(scroll_area)
        
        return final_container
        
    def paste_clipboard(self):
        """从剪贴板粘贴内容到邮箱输入框"""
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            current = self.email_input.toPlainText()
            if current and not current.endswith('\n'):
                current += '\n'
            self.email_input.setPlainText(current + text)
            self.log_info("剪贴板操作", "已从剪贴板粘贴内容到邮箱输入框")
        else:
            self.log_warning("剪贴板操作", "剪贴板中没有文本内容")

    # This method is no longer needed with the new UI design
    # All functionality has been integrated directly into create_invite_tab

    def create_manage_tab(self) -> QWidget:
        """创建团队管理标签页"""
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # 创建内容widget
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # 控制按钮区域
        control_widget = QWidget()
        control_widget.setFixedHeight(60)  # 固定高度
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setSpacing(15)

        self.load_data_btn = StyleManager.create_button(
            "🔄 获取团队数据", "primary"
        )
        self.load_data_btn.clicked.connect(self.load_team_data)

        self.refresh_btn = StyleManager.create_button(
            "🔃 刷新数据", "secondary"
        )
        self.refresh_btn.clicked.connect(self.refresh_team_data)

        control_layout.addWidget(self.load_data_btn)
        control_layout.addWidget(self.refresh_btn)
        control_layout.addStretch()

        control_widget.setLayout(control_layout)
        layout.addWidget(control_widget)

        # 数据显示区域
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setHandleWidth(10)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background: #dee2e6;
                border-radius: 5px;
                margin: 2px;
            }
            QSplitter::handle:hover {
                background: #007bff;
            }
        """)

        # 团队成员表格
        members_group = QGroupBox("👥 团队成员")
        members_layout = QVBoxLayout()
        members_layout.setSpacing(15)
        members_layout.setContentsMargins(25, 30, 25, 25)

        # 成员统计信息
        members_stats = self.create_members_stats_widget()
        members_layout.addWidget(members_stats)

        # 创建表格容器
        table_container = QWidget()
        table_container.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 20px;
                border: 2px solid rgba(59, 130, 246, 0.1);
            }
        """)
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(2, 2, 2, 2)

        self.members_table = QTableWidget()
        self.members_table.setColumnCount(5)
        self.members_table.setHorizontalHeaderLabels(["序号", "ID", "邮箱", "角色", "加入时间"])
        self.members_table.setMinimumHeight(300)  # 增加最小高度，确保表格可见

        # 优化表格列宽设置，确保内容完整显示
        header = self.members_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # 序号列固定宽度
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)  # ID列可调整
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # 邮箱列拉伸
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # 角色列固定宽度
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive)  # 时间列可调整

        # 设置列宽
        self.members_table.setColumnWidth(0, 80)   # 序号列
        self.members_table.setColumnWidth(1, 220)  # ID列
        self.members_table.setColumnWidth(3, 120)  # 角色列
        self.members_table.setColumnWidth(4, 200)  # 时间列

        # 美化表格样式
        self.members_table.setStyleSheet(f"""
            QTableWidget {{
                background: {StyleManager.BACKGROUND_COLOR};
                border: none;
                border-radius: 12px;
                gridline-color: {StyleManager.NEUTRAL_MEDIUM};
                outline: none;
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {StyleManager.NEUTRAL_MEDIUM};
                font-size: 13px;
            }}
            QTableWidget::item:selected {{
                background: {StyleManager.PRIMARY_COLOR}15;
                color: {StyleManager.PRIMARY_COLOR};
                font-weight: 500;
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {StyleManager.PRIMARY_COLOR}, stop:1 {StyleManager.PRIMARY_LIGHT});
                color: white;
                font-weight: 500;
                font-size: 13px;
                padding: 12px;
                border: none;
            }}
            QHeaderView::section:first {{
                border-top-left-radius: 12px;
            }}
            QHeaderView::section:last {{
                border-top-right-radius: 12px;
            }}
        """)

        self.members_table.setAlternatingRowColors(True)
        self.members_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.members_table.verticalHeader().setVisible(False)
        self.members_table.setShowGrid(True)
        self.members_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # 设置行高以确保内容完整显示
        self.members_table.verticalHeader().setDefaultSectionSize(50)
        
        table_layout.addWidget(self.members_table)
        members_layout.addWidget(table_container)

        # 添加表格容器阴影
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(59, 130, 246, 30))
        table_container.setGraphicsEffect(shadow)

        members_group.setLayout(members_layout)
        StyleManager.apply_shadow_effect(members_group, blur_radius=8, offset=(0, 3))
        splitter.addWidget(members_group)

        # 邀请记录表格
        invitations_group = QGroupBox("📨 邀请记录")
        invitations_layout = QVBoxLayout()
        invitations_layout.setSpacing(15)
        invitations_layout.setContentsMargins(25, 30, 25, 25)

        # 邀请统计信息
        invitations_stats = self.create_invitations_stats_widget()
        invitations_layout.addWidget(invitations_stats)

        # 查询操作按钮区域
        query_control_layout = QHBoxLayout()
        query_control_layout.setContentsMargins(0, 5, 0, 15)
        query_control_layout.setSpacing(15)

        # 创建按钮容器
        button_container = QWidget()
        button_container.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.8);
                border-radius: 20px;
                border: 2px solid rgba(59, 130, 246, 0.1);
            }
        """)
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(15, 10, 15, 10)
        button_layout.setSpacing(15)

        self.query_pending_emails_btn = StyleManager.create_button(
            "🔍 查询未接受邮箱", "primary"
        )
        self.query_pending_emails_btn.clicked.connect(self.query_pending_emails)
        self.query_pending_emails_btn.setToolTip("查询所有未接受邀请的邮箱地址")

        # 添加调试按钮
        self.debug_data_btn = StyleManager.create_button(
            "🔧 调试数据", "warning"
        )
        self.debug_data_btn.clicked.connect(self.debug_current_data)
        self.debug_data_btn.setToolTip("调试当前数据结构和统计计算")

        button_layout.addWidget(self.query_pending_emails_btn)
        button_layout.addWidget(self.debug_data_btn)
        button_layout.addStretch()

        query_control_layout.addWidget(button_container)
        invitations_layout.addLayout(query_control_layout)

        # 创建表格容器
        table_container = QWidget()
        table_container.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 20px;
                border: 2px solid rgba(59, 130, 246, 0.1);
            }
        """)
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(2, 2, 2, 2)

        self.invitations_table = QTableWidget()
        self.invitations_table.setColumnCount(4)
        self.invitations_table.setHorizontalHeaderLabels(["序号", "ID", "邮箱", "邀请时间"])
        self.invitations_table.setMinimumHeight(300)  # 增加最小高度，确保表格可见

        # 优化邀请表格列宽设置
        inv_header = self.invitations_table.horizontalHeader()
        inv_header.setStretchLastSection(True)
        inv_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # 序号列固定宽度
        inv_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)  # ID列可调整
        inv_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # 邮箱列拉伸
        inv_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)  # 时间列可调整

        # 设置列宽
        self.invitations_table.setColumnWidth(0, 80)   # 序号列
        self.invitations_table.setColumnWidth(1, 220)  # ID列
        self.invitations_table.setColumnWidth(3, 200)  # 时间列

        # 美化表格样式
        self.invitations_table.setStyleSheet(f"""
            QTableWidget {{
                background: {StyleManager.BACKGROUND_COLOR};
                border: none;
                border-radius: 12px;
                gridline-color: {StyleManager.NEUTRAL_MEDIUM};
                outline: none;
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {StyleManager.NEUTRAL_MEDIUM};
                font-size: 13px;
            }}
            QTableWidget::item:selected {{
                background: {StyleManager.PRIMARY_COLOR}15;
                color: {StyleManager.PRIMARY_COLOR};
                font-weight: 500;
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {StyleManager.PRIMARY_COLOR}, stop:1 {StyleManager.PRIMARY_LIGHT});
                color: white;
                font-weight: 500;
                font-size: 13px;
                padding: 12px;
                border: none;
            }}
            QHeaderView::section:first {{
                border-top-left-radius: 12px;
            }}
            QHeaderView::section:last {{
                border-top-right-radius: 12px;
            }}
        """)

        self.invitations_table.setAlternatingRowColors(True)
        self.invitations_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.invitations_table.verticalHeader().setVisible(False)
        self.invitations_table.setShowGrid(True)
        self.invitations_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # 设置行高以确保内容完整显示
        self.invitations_table.verticalHeader().setDefaultSectionSize(50)
        
        table_layout.addWidget(self.invitations_table)
        invitations_layout.addWidget(table_container)

        # 添加表格容器阴影
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(59, 130, 246, 30))
        table_container.setGraphicsEffect(shadow)

        invitations_group.setLayout(invitations_layout)
        StyleManager.apply_shadow_effect(invitations_group, blur_radius=8, offset=(0, 3))
        splitter.addWidget(invitations_group)

        # 设置分割器比例，调整为更合理的显示比例
        splitter.setSizes([500, 400])

        layout.addWidget(splitter)

        # 添加弹性空间
        layout.addStretch()
        content_widget.setLayout(layout)

        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)

        # 创建主容器
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        main_widget.setLayout(main_layout)

        return main_widget

    def create_members_stats_widget(self):
        """创建简化版成员统计组件"""
        stats_widget = QWidget()
        stats_layout = QHBoxLayout()
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(10)  # 减小卡片间距

        # 使用更简洁的图标
        self.total_members_card = StyleManager.create_stat_card("👥", "总成员", "0", "#4361ee")
        self.active_members_card = StyleManager.create_stat_card("✅", "已加入", "0", "#22c55e")
        self.pending_members_card = StyleManager.create_stat_card("⏳", "待加入", "0", "#f97316")

        # 设置每个卡片的宽度比例
        self.total_members_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.active_members_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.pending_members_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        stats_layout.addWidget(self.total_members_card)
        stats_layout.addWidget(self.active_members_card)
        stats_layout.addWidget(self.pending_members_card)
        stats_layout.addStretch()

        stats_widget.setLayout(stats_layout)
        return stats_widget

    def create_invitations_stats_widget(self):
        """创建简化版邀请统计组件"""
        stats_widget = QWidget()
        stats_layout = QHBoxLayout()
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(10)  # 减小卡片间距

        # 使用更简洁的图标
        self.total_invitations_card = StyleManager.create_stat_card("📨", "总邀请", "0", "#4361ee")
        self.recent_invitations_card = StyleManager.create_stat_card("🕒", "今日邀请", "0", "#f97316")

        # 设置每个卡片的宽度比例
        self.total_invitations_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.recent_invitations_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        stats_layout.addWidget(self.total_invitations_card)
        stats_layout.addWidget(self.recent_invitations_card)
        stats_layout.addStretch()

        stats_widget.setLayout(stats_layout)
        return stats_widget

    def create_batch_tab(self) -> QWidget:
        """创建批量操作标签页"""
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # 创建内容widget
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # 警告区域
        warning_widget = self.create_warning_widget()
        warning_widget.setFixedHeight(100)  # 固定高度
        layout.addWidget(warning_widget)

        # 批量删除区域
        batch_group = QGroupBox("🔄 批量操作")
        batch_group.setMinimumHeight(280)  # 设置最小高度
        batch_layout = QVBoxLayout()
        batch_layout.setSpacing(20)

        # 操作按钮网格
        button_grid = QGridLayout()
        button_grid.setSpacing(15)

        # 创建全新操作按钮
        self.batch_delete_unjoined_btn = self.create_batch_button(
            "🗑️ 删除未加入成员",
            "删除所有未加入团队的成员",
            [StyleManager.WARNING_COLOR, StyleManager.WARNING_LIGHT],
            self.batch_delete_unjoined_members
        )

        self.batch_delete_invitations_btn = self.create_batch_button(
            "📧 删除邀请记录",
            "删除所有待处理的邀请记录",
            [StyleManager.PRIMARY_COLOR, StyleManager.PRIMARY_LIGHT],
            self.batch_delete_invitations
        )

        self.batch_delete_all_btn = self.create_batch_button(
            "🚫 删除所有未确认",
            "删除所有未加入成员和邀请记录",
            [StyleManager.DANGER_COLOR, StyleManager.DANGER_LIGHT],
            self.batch_delete_all_unconfirmed
        )

        self.switch_to_community_plan_btn = self.create_batch_button(
            "🔄 切换到社区计划",
            "将当前登录账号切换到社区计划",
            [StyleManager.SUCCESS_COLOR, StyleManager.SUCCESS_LIGHT],
            self.switch_to_community_plan
        )

        self.switch_to_max_plan_btn = self.create_batch_button(
            "⭐ 切换到 Max 计划",
            "将当前登录账号切换到 Max 计划",
            [StyleManager.INFO_COLOR, StyleManager.INFO_LIGHT],
            self.switch_to_max_plan
        )

        button_grid.addWidget(self.batch_delete_unjoined_btn, 0, 0)
        button_grid.addWidget(self.batch_delete_invitations_btn, 0, 1)
        button_grid.addWidget(self.batch_delete_all_btn, 1, 0)
        button_grid.addWidget(self.switch_to_community_plan_btn, 1, 1)
        button_grid.addWidget(self.switch_to_max_plan_btn, 2, 0)

        batch_layout.addLayout(button_grid)

        batch_group.setLayout(batch_layout)
        StyleManager.apply_shadow_effect(batch_group, blur_radius=8, offset=(0, 3))
        layout.addWidget(batch_group)

        # 操作日志区域
        log_group = QGroupBox("📋 操作日志")
        log_group.setMinimumHeight(280)  # 设置最小高度
        log_layout = QVBoxLayout()

        # 日志控制按钮
        log_control_layout = QHBoxLayout()

        clear_log_btn = QPushButton("🧹 清空日志")
        clear_log_btn.clicked.connect(lambda: self.batch_log.clear())
        clear_log_btn.setStyleSheet("""
            QPushButton {
                background: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #5a6268;
            }
        """)

        log_control_layout.addWidget(clear_log_btn)
        log_control_layout.addStretch()

        log_layout.addLayout(log_control_layout)

        self.batch_log = QTextEdit()
        self.batch_log.setReadOnly(True)
        self.batch_log.setFixedHeight(180)  # 固定高度
        self.batch_log.setStyleSheet("""
            QTextEdit {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #ffffff, stop: 1 #f8f9fa);
                border: 2px solid rgba(79, 172, 254, 0.2);
                border-radius: 8px;
                padding: 8px;
                color: #495057;
            }
        """)
        log_layout.addWidget(self.batch_log)

        log_group.setLayout(log_layout)
        StyleManager.apply_shadow_effect(log_group, blur_radius=8, offset=(0, 3))
        layout.addWidget(log_group)

        # 添加弹性空间
        layout.addStretch()
        content_widget.setLayout(layout)

        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)

        # 创建主容器
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        main_widget.setLayout(main_layout)

        return main_widget

    def create_warning_widget(self):
        """创建警告组件"""
        warning_widget = QWidget()
        warning_widget.setStyleSheet(f"""
            QWidget {{
                background: {StyleManager.WARNING_LIGHT}30;
                border: 1px solid {StyleManager.WARNING_COLOR}40;
                border-radius: 8px;
                border-left: 5px solid {StyleManager.WARNING_COLOR};
            }}
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)

        # 警告图标
        icon_label = QLabel("⚠️")
        icon_label.setStyleSheet("font-size: 24px;")

        # 警告文本
        warning_text = QLabel(
            "<b>重要提醒：</b><br>"
            "• 批量操作不可撤销，请谨慎使用<br>"
            "• 建议在操作前先备份重要数据<br>"
            "• 确保您有足够的权限执行这些操作"
        )
        warning_text.setStyleSheet(f"""
            QLabel {{
                color: {StyleManager.WARNING_DARK};
                font-size: 14px;
                background: transparent;
                border: none;
            }}
        """)

        layout.addWidget(icon_label)
        layout.addWidget(warning_text)
        layout.addStretch()

        warning_widget.setLayout(layout)
        StyleManager.apply_shadow_effect(warning_widget, blur_radius=5, offset=(0, 2))

        return warning_widget

    def create_batch_button(self, title, description, colors, callback=None):
        """创建批量操作按钮"""
        button_widget = QWidget()
        button_widget.setFixedHeight(100)
        button_widget.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 {colors[0]}, stop: 1 {colors[1]});
                border-radius: 8px;
                color: white;
            }}
            QWidget:hover {{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 {colors[1]}, stop: 1 {colors[0]});
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)

        # 标题
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: white;
                background: transparent;
            }
        """)

        # 描述
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: rgba(255, 255, 255, 0.8);
                background: transparent;
            }
        """)
        desc_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()

        button_widget.setLayout(layout)
        StyleManager.apply_shadow_effect(button_widget, blur_radius=5, offset=(0, 2))

        # 使按钮可点击
        if callback:
            button_widget.mousePressEvent = lambda event: callback() if event.button() == Qt.MouseButton.LeftButton else None
            button_widget.setCursor(Qt.CursorShape.PointingHandCursor)

        return button_widget

    def create_data_tab(self) -> QWidget:
        """创建数据查看标签页"""
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # 创建内容widget
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # 原始数据显示
        data_group = QGroupBox("📊 原始数据")
        data_layout = QVBoxLayout()

        # 控制按钮
        control_layout = QHBoxLayout()
        control_layout.setSpacing(15)

        self.export_data_btn = StyleManager.create_button(
            "📤 导出数据", "primary"
        )
        self.export_data_btn.clicked.connect(self.export_team_data)

        self.format_data_btn = StyleManager.create_button(
            "🎨 格式化显示", "secondary"
        )
        self.format_data_btn.clicked.connect(self.format_data_display)

        control_layout.addWidget(self.export_data_btn)
        control_layout.addWidget(self.format_data_btn)
        control_layout.addStretch()

        data_layout.addLayout(control_layout)

        # 数据显示区域
        self.raw_data_display = QTextEdit()
        self.raw_data_display.setReadOnly(True)
        self.raw_data_display.setFont(QFont("Consolas", 9))
        self.raw_data_display.setMinimumHeight(400)
        self.raw_data_display.setStyleSheet("""
            QTextEdit {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #ffffff, stop: 1 #f8f9fa);
                border: 2px solid rgba(79, 172, 254, 0.2);
                border-radius: 8px;
                padding: 12px;
                color: #495057;
                line-height: 1.4;
            }
        """)
        data_layout.addWidget(self.raw_data_display)

        data_group.setLayout(data_layout)
        StyleManager.apply_shadow_effect(data_group, blur_radius=8, offset=(0, 3))
        layout.addWidget(data_group)

        # 添加弹性空间
        layout.addStretch()
        content_widget.setLayout(layout)

        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)

        # 创建主容器
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        main_widget.setLayout(main_layout)

        return main_widget

    # ==================== 事件处理方法 ====================

    def validate_emails_realtime(self):
        """实时验证邮箱"""
        text = self.email_input.toPlainText().strip()
        if not text:
            # 重置所有计数器并禁用按钮
            self.total_emails_card.value_label.setText("0")
            self.valid_emails_card.value_label.setText("0")
            self.invalid_emails_card.value_label.setText("0")
            self.invite_btn.setEnabled(False)
            self.validation_progress.setValue(0)
            return

        emails = [email.strip() for email in text.split('\n') if email.strip()]
        total = len(emails)
        
        # 显示验证进度
        self.validation_progress.setValue(10)  # 初始进度
        
        # 批量验证并显示进度动画
        valid = 0
        invalid = 0
        
        for i, email in enumerate(emails):
            # 更新进度
            progress = int(10 + (i / total) * 80)
            self.validation_progress.setValue(progress)
            QApplication.processEvents()  # 允许UI更新
            
            # 验证邮箱
            if self.api_client.validate_email(email):
                valid += 1
            else:
                invalid += 1
        
        # 验证完成
        self.validation_progress.setValue(100)
        
        # 更新统计卡片
        self.total_emails_card.value_label.setText(str(total))
        self.valid_emails_card.value_label.setText(str(valid))
        self.invalid_emails_card.value_label.setText(str(invalid))

        # 更新按钮状态
        self.invite_btn.setEnabled(valid > 0)
        
        # 根据验证结果设置进度条颜色
        if total > 0:
            if valid == total:  # 全部有效
                self.validation_progress.setStyleSheet(f"""
                    QProgressBar::chunk {{
                        background: {StyleManager.SUCCESS_COLOR};
                    }}
                """)
            elif valid == 0:  # 全部无效
                self.validation_progress.setStyleSheet(f"""
                    QProgressBar::chunk {{
                        background: {StyleManager.DANGER_COLOR};
                    }}
                """)
            else:  # 部分有效
                self.validation_progress.setStyleSheet(f"""
                    QProgressBar::chunk {{
                        background: {StyleManager.WARNING_COLOR};
                    }}
                """)
        
        # 记录验证结果
        validation_msg = f"邮箱验证: 总数: {total}, 有效: {valid}, 无效: {invalid}"
        if valid == total:
            self.log_success("邮箱验证", validation_msg)
        elif valid == 0:
            self.log_error("邮箱验证", validation_msg)
        else:
            self.log_warning("邮箱验证", validation_msg)



    def clear_email_input(self):
        """清空邮箱输入"""
        self.email_input.clear()
        self.validate_emails_realtime()

    def invite_members(self):
        """邀请成员"""
        text = self.email_input.toPlainText().strip()
        if not text:
            self.log_warning("邀请失败", "请输入邮箱地址")
            return

        emails = [email.strip() for email in text.split('\n') if email.strip()]
        valid_emails = [email for email in emails if self.api_client.validate_email(email)]
        invalid_emails = [email for email in emails if not self.api_client.validate_email(email)]

        if invalid_emails:
            self.log_warning("发现无效邮箱", f"发现 {len(invalid_emails)} 个无效邮箱: {', '.join(invalid_emails[:5])}")
            if len(invalid_emails) > 5:
                self.log_info("无效邮箱详情", f"还有 {len(invalid_emails) - 5} 个无效邮箱未显示")

        if not valid_emails:
            self.log_warning("邀请失败", "没有找到有效的邮箱地址")
            return

        self.log_info("开始邀请", f"准备邀请 {len(valid_emails)} 个有效邮箱")
        # 启动工作线程
        self.start_worker_thread("invite_members", emails=valid_emails)

    def load_team_data(self):
        """加载团队数据"""
        self.start_worker_thread("get_team_data")

    def refresh_team_data(self):
        """刷新团队数据"""
        if self.team_data is not None:
            self.log_info("刷新数据", "正在刷新团队数据...")
            self.load_team_data()
        else:
            self.log_warning("刷新失败", "请先加载团队数据")

    def batch_delete_unjoined_members(self):
        """批量删除未加入成员"""
        if not self.team_data:
            self.log_warning("操作失败", "请先加载团队数据")
            return

        unjoined_ids = self.get_unjoined_member_ids()
        if not unjoined_ids:
            self.log_info("批量删除", "没有找到未加入的成员")
            return

        self.log_warning("批量删除确认", f"准备删除 {len(unjoined_ids)} 个未加入成员，此操作不可撤销！")
        self.log_batch_operation(f"开始批量删除 {len(unjoined_ids)} 个未加入成员")
        self.start_worker_thread("batch_delete", member_ids=unjoined_ids)

    def batch_delete_invitations(self):
        """批量删除邀请记录"""
        if not self.team_data:
            self.log_warning("操作失败", "请先加载团队数据")
            return

        invitation_ids = self.get_invitation_ids()
        if not invitation_ids:
            self.log_info("批量删除", "没有找到邀请记录")
            return

        self.log_warning("批量删除确认", f"准备删除 {len(invitation_ids)} 条邀请记录，此操作不可撤销！")
        self.log_batch_operation(f"开始批量删除 {len(invitation_ids)} 条邀请记录")
        self.start_worker_thread("batch_delete", member_ids=invitation_ids)

    def batch_delete_all_unconfirmed(self):
        """批量删除所有未确认的成员和邀请"""
        if not self.team_data:
            self.log_warning("操作失败", "请先加载团队数据")
            return

        unjoined_ids = self.get_unjoined_member_ids()
        invitation_ids = self.get_invitation_ids()
        all_ids = unjoined_ids + invitation_ids

        if not all_ids:
            self.log_info("批量删除", "没有找到未确认的成员或邀请")
            return

        self.log_warning("批量删除确认",
                        f"准备删除所有未确认的成员和邀请 - "
                        f"未加入成员: {len(unjoined_ids)} 个, "
                        f"邀请记录: {len(invitation_ids)} 条, "
                        f"总计: {len(all_ids)} 项，此操作不可撤销！")
        self.log_batch_operation(f"开始批量删除所有未确认项目，共 {len(all_ids)} 项")
        self.start_worker_thread("batch_delete", member_ids=all_ids)

    def switch_to_community_plan(self):
        """切换到社区计划"""
        self.log_info("计划切换", "准备将当前账号切换到社区计划...")
        self.log_batch_operation("开始切换账号到社区计划")
        self.start_worker_thread("put_user_on_community_plan")

    def switch_to_max_plan(self):
        """切换到 Max 计划"""
        self.log_info("计划切换", "准备将当前账号切换到 Max 计划...")
        self.log_batch_operation("开始切换账号到 Max 计划")
        self.start_worker_thread("put_user_on_max_plan")

    def export_team_data(self):
        """导出团队数据"""
        if not self.team_data:
            self.log_warning("导出失败", "没有数据可导出，请先加载团队数据")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出团队数据",
            f"team_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON文件 (*.json);;所有文件 (*)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.team_data, f, indent=2, ensure_ascii=False)
                self.log_success("导出成功", f"数据已导出到: {file_path}")
            except Exception as e:
                self.log_error("导出失败", f"导出失败: {str(e)}")

    def debug_current_data(self):
        """调试当前数据结构"""
        print("\n" + "="*60)
        print("🔍 调试当前数据结构")
        print("="*60)

        if not self.team_data:
            print("❌ 没有数据可调试")
            self.log_warning("调试", "没有数据可调试，请先加载团队数据")
            return

        print("📊 原始数据结构:")
        import json
        print(json.dumps(self.team_data, indent=2, ensure_ascii=False))

        print("\n🔍 数据提取测试:")

        # 测试用户提取
        users = self.extract_users_from_data(self.team_data)
        print(f"   提取到的用户数: {len(users)}")
        for i, user in enumerate(users):
            joined = "已加入" if user.get('joinedAt') else "未加入"
            print(f"     {i+1}. {user.get('email', 'N/A')} - {joined}")

        # 测试邀请提取
        invitations = self.extract_invitations_from_data(self.team_data)
        print(f"   提取到的邀请数: {len(invitations)}")
        for i, invitation in enumerate(invitations):
            print(f"     {i+1}. {invitation.get('email', 'N/A')} - {invitation.get('invitedAt', 'N/A')}")

        # 测试统计计算
        print("\n📊 统计计算:")
        total_members = len(users)
        pending_members = len([u for u in users if not u.get('joinedAt')])
        active_members = total_members - pending_members

        print(f"   总成员数: {total_members}")
        print(f"   活跃成员数: {active_members}")
        print(f"   待加入成员数: {pending_members}")
        print(f"   邀请记录数: {len(invitations)}")

        # 按照正确的业务逻辑
        print(f"\n🎯 正确的统计逻辑:")
        print(f"   待加入人数 = 邀请记录中的人数 = {len(invitations)}")
        print(f"   邀请记录中的总邀请 = 待加入人数 = {len(invitations)}")
        print(f"   说明：未加入的人就是被邀请但还没加入的人")

        # 检查今日邀请
        from datetime import datetime, date
        today = date.today()
        today_invited = 0
        for invitation in invitations:
            invited_at = invitation.get('invitedAt')
            if invited_at:
                try:
                    if isinstance(invited_at, (int, float)):
                        invite_date = datetime.fromtimestamp(invited_at / 1000).date()
                        print(f"     邀请时间: {invite_date} (今天: {today})")
                        if invite_date == today:
                            today_invited += 1
                except Exception as e:
                    print(f"     时间解析错误: {e}")

        print(f"   今日邀请数: {today_invited}")

        # 手动调用统计更新
        print("\n🔄 手动更新统计...")
        self.update_statistics(users, invitations)

        self.log_info("调试完成", f"用户{len(users)}个，邀请{len(invitations)}个，待加入{pending_members}个")
        print("\n" + "="*60)

    def query_pending_emails(self):
        """查询未接受邀请的邮箱"""
        if not self.team_data:
            self.log_warning("查询失败", "没有数据可查询，请先加载团队数据")
            return

        # 获取所有邀请记录
        invitations = self.extract_invitations_from_data(self.team_data)

        if not invitations:
            self.log_info("查询结果", "没有找到未接受的邀请记录")
            return

        # 提取邮箱地址
        pending_emails = []
        for invitation in invitations:
            email = invitation.get('email', '').strip()
            if email and email not in pending_emails:
                pending_emails.append(email)

        if not pending_emails:
            self.log_info("查询结果", "没有找到有效的邮箱地址")
            return

        # 在日志中显示查询结果
        self.log_success("查询完成", f"找到 {len(pending_emails)} 个未接受邀请的邮箱")

        # 显示专门的邮箱列表弹窗
        try:
            emails_dialog = PendingEmailsDialog(pending_emails, self)
            emails_dialog.show()
            self.log_info("邮箱弹窗", "已打开邮箱列表弹窗，您可以在弹窗中查看、复制或导出邮箱列表")
        except Exception as e:
            # 如果弹窗创建失败，回退到日志显示
            self.log_warning("弹窗显示失败", f"无法创建邮箱列表弹窗: {str(e)}")
            email_list = '\n'.join(pending_emails)
            self.log_info("邮箱列表", f"未接受邀请的邮箱（每行一个，方便复制）:\n{email_list}")

    def format_data_display(self):
        """格式化显示数据"""
        if self.team_data:
            formatted_data = json.dumps(self.team_data, indent=2, ensure_ascii=False)
            self.raw_data_display.setPlainText(formatted_data)
        else:
            self.raw_data_display.setPlainText("没有数据")

    # ==================== 工具方法 ====================

    def start_worker_thread(self, operation: str, **kwargs):
        """启动工作线程 - 增强版2.0"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.log_warning("操作冲突", "有操作正在进行中，请稍候...")
            return

        # 操作名称映射
        operation_names = {
            "get_team_data": "获取团队数据",
            "invite_members": "邀请成员",
            "batch_delete": "批量删除",
            "put_user_on_community_plan": "切换到社区计划"
        }
        
        # 操作状态文本映射
        operation_status = {
            "get_team_data": "正在连接服务器获取团队数据...",
            "invite_members": "正在发送邀请请求...",
            "batch_delete": "正在执行批量删除操作，请稍候...",
            "put_user_on_community_plan": "正在切换账号计划类型..."
        }
        
        # 显示加载覆盖层
        op_name = operation_names.get(operation, operation)
        op_status = operation_status.get(operation, "正在处理请求...")
        self.show_loading(f"正在{op_name}", op_status)

        # 创建并配置工作线程
        self.worker_thread = WorkerThread(self.api_client, operation, **kwargs)
        self.worker_thread.finished.connect(self.on_worker_finished)
        self.worker_thread.progress.connect(self.on_worker_progress)

        # 更新状态栏信息
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText(f"正在执行: {op_name}")

        # 禁用相关按钮
        self.set_buttons_enabled(False)

        # 记录操作开始
        self.log_info("操作开始", f"正在执行: {op_name}")

        # 启动线程
        self.worker_thread.start()

    def on_worker_finished(self, success: bool, message: str, data: Any):
        """工作线程完成回调 - 增强版2.0"""
        # 隐藏加载覆盖层
        self.hide_loading()
        
        # 重置状态栏
        self.progress_bar.setVisible(False)
        self.status_label.setText("就绪")

        # 启用按钮
        self.set_buttons_enabled(True)

        if success:
            if data is not None:  # 获取数据操作
                self.team_data = data
                self.log_info("数据更新", "正在处理和显示团队数据...")
                
                try:
                    # 更新界面显示
                    self.update_team_display()
                    
                    # 更新连接状态和通知
                    self.update_connection_status(True)
                    self.status_label.setText("✅ 数据加载成功")

                    # 显示成功提示
                    self.show_notification("✅ 数据加载成功", "团队数据已成功更新", "success")
                    
                    # 记录成功日志
                    self.log_success("数据加载成功", "团队数据已更新")
                except Exception as e:
                    self.log_error("数据显示错误", f"显示数据时发生错误: {str(e)}")
                    print(f"显示数据时发生错误: {str(e)}")
            else:  # 其他操作
                if "邀请" in message:
                    self.log_invite_history(message)
                    self.log_success("邀请成功", message)
                    self.show_notification("✅ 邀请成功", message, "success")
                elif "删除" in message:
                    self.log_batch_operation(message)
                    self.log_success("操作完成", message)
                    self.show_notification("✅ 操作完成", message, "success")
                    # 自动刷新数据
                    if self.team_data:
                        self.load_team_data()
                else:
                    self.log_success("操作完成", message)
                    self.show_notification("✅ 操作完成", message, "success")
        else:
            self.update_connection_status(False)
            self.log_error("操作失败", message)
            self.show_notification("❌ 操作失败", message, "error")

            # 详细的错误分析和建议
            if "401" in message or "unauthorized" in message.lower():
                self.log_warning("认证问题", "Cookie可能已过期，请在配置中更新Cookie")
                self.show_notification("🔑 认证失败", "Cookie可能已过期，请更新配置", "warning")
            elif "403" in message or "forbidden" in message.lower():
                self.log_warning("权限问题", "当前账号可能没有团队管理权限")
                self.show_notification("🚫 权限不足", "账号可能没有团队管理权限", "warning")
            elif "404" in message or "not found" in message.lower():
                self.log_warning("API问题", "API端点可能不存在，请检查配置")
                self.show_notification("🔍 API错误", "API端点不存在，请检查配置", "warning")
            elif "timeout" in message.lower():
                self.log_warning("网络问题", "连接超时，请检查网络连接")
                self.show_notification("⏱️ 连接超时", "网络连接超时，请检查网络", "warning")
            elif "json" in message.lower():
                self.log_warning("响应问题", "服务器返回了非JSON格式的响应，可能是认证问题")
                self.show_notification("📄 响应错误", "服务器响应格式错误", "warning")
            
    def show_notification(self, title, message, type="info"):
        """显示通知消息"""
        notification = QWidget(self)

        # 根据类型设置不同的颜色
        if type == "success":
            bg_color = StyleManager.SUCCESS_COLOR
            icon = "✅"
        elif type == "error":
            bg_color = StyleManager.DANGER_COLOR
            icon = "❌"
        elif type == "warning":
            bg_color = StyleManager.WARNING_COLOR
            icon = "⚠️"
        else:
            bg_color = StyleManager.PRIMARY_COLOR
            icon = "ℹ️"

        notification.setStyleSheet(f"""
            QWidget {{
                background: white;
                border-radius: 15px;
                border-left: 6px solid {bg_color};
            }}
        """)

        # 创建通知布局
        layout = QVBoxLayout(notification)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        # 标题行
        title_layout = QHBoxLayout()
        title_label = QLabel(f"{icon} {title}")
        title_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 700;
            color: {bg_color};
        """)

        close_btn = QPushButton("×")
        close_btn.setFixedSize(25, 25)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: {bg_color}20;
                color: {bg_color};
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {bg_color}40;
            }}
        """)
        close_btn.clicked.connect(notification.deleteLater)

        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_btn)

        # 消息内容
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet("""
            font-size: 14px;
            color: #475569;
        """)
        # 设置最大宽度以确保合理的换行
        msg_label.setMaximumWidth(350)

        layout.addLayout(title_layout)
        layout.addWidget(msg_label)

        # 根据内容自动调整大小
        notification.adjustSize()

        # 设置最小和最大尺寸限制
        notification.setMinimumSize(300, 80)
        notification.setMaximumSize(400, 300)

        # 确保通知窗口大小合适
        if notification.height() < 120:
            notification.setFixedHeight(120)

        # 应用阴影
        StyleManager.apply_shadow_effect(notification, blur_radius=15, offset=(0, 5))

        # 设置位置并显示
        notification.move(self.width() - notification.width() - 20, 70)
        notification.show()

        # 设置自动关闭定时器
        QTimer.singleShot(5000, notification.deleteLater)

    def update_connection_status(self, connected: bool):
        """更新连接状态 - 统一版本"""
        # 更新全局连接状态标志
        self.is_connected = connected
        
        if connected:
            # 状态栏显示
            self.connection_label.setText("🟢 已连接")
            self.connection_label.setStyleSheet(f"""
                color: {StyleManager.SUCCESS_COLOR};
                font-weight: 700;
                padding-right: 10px;
            """)
            
            # 更新主界面状态
            if hasattr(self, 'connection_status') and self.connection_status is not None:
                # 更改为新风格状态控件 - 已连接状态
                self.connection_status.setText("🟢 已连接")
                self.connection_status.setStyleSheet("""
                    QLabel {
                        background: rgba(238, 219, 205, 0.8);
                        border: 2px solid #43e97b;
                        border-radius: 20px;
                        padding: 12px 25px;
                        font-weight: 600;
                        font-size: 16px;
                        color: #22c55e;
                    }
                """)
                
                # 为状态控件添加鼠标悬浮效果
                self.connection_status.setToolTip("连接状态正常，可以正常访问API")
                
                # 添加阴影效果
                StyleManager.apply_shadow_effect(self.connection_status, blur_radius=10, offset=(0, 3))
                
            # 显示成功通知
            current_time = datetime.now().strftime('%H:%M:%S')
            self.show_notification(
                "🌐 连接成功", 
                f"API连接状态正常，服务器响应正常。\n连接时间: {current_time}", 
                "success"
            )
        else:
            # 状态栏显示
            self.connection_label.setText("🔴 未连接")
            self.connection_label.setStyleSheet(f"""
                color: {StyleManager.DANGER_COLOR};
                font-weight: 700;
                padding-right: 10px;
            """)
            
            # 更新主界面状态
            if hasattr(self, 'connection_status') and self.connection_status is not None:
                self.connection_status.setText("🔴 未连接")
                self.connection_status.setStyleSheet("""
                    QLabel {
                        background: rgba(93, 102, 217, 0.8);
                        border-radius: 20px;
                        padding: 12px 25px;
                        color: white;
                        font-size: 16px;
                        font-weight: 600;
                    }
                """)
                
                # 为状态控件添加鼠标悬浮效果
                self.connection_status.setToolTip("API连接失败，请检查网络或API配置")
                
                # 添加阴影效果
                StyleManager.apply_shadow_effect(self.connection_status, blur_radius=10, offset=(0, 3))
                
            # 显示错误通知
            self.show_notification(
                "🚫 连接失败", 
                "无法连接到API服务器，请检查网络连接或API配置。\n您可以在「工具」菜单中打开「配置设置」检查API配置。", 
                "error"
            )

    # 通知方法已替换为日志系统

    def on_worker_progress(self, progress: int, status: str):
        """工作线程进度回调"""
        self.progress_bar.setValue(progress)
        self.status_label.setText(status)

    def set_buttons_enabled(self, enabled: bool):
        """设置按钮启用状态"""
        self.invite_btn.setEnabled(enabled)
        self.load_data_btn.setEnabled(enabled)
        self.refresh_btn.setEnabled(enabled)
        self.batch_delete_unjoined_btn.setEnabled(enabled)
        self.batch_delete_invitations_btn.setEnabled(enabled)
        self.batch_delete_all_btn.setEnabled(enabled)
        self.switch_to_community_plan_btn.setEnabled(enabled)
        self.switch_to_max_plan_btn.setEnabled(enabled)

    def get_unjoined_member_ids(self) -> List[str]:
        """获取未加入成员的ID列表"""
        if not self.team_data:
            return []

        ids = []
        users = self.extract_users_from_data(self.team_data)
        for user in users:
            if not user.get('role'):  # 没有角色表示未加入
                ids.append(user.get('id', ''))

        return [id for id in ids if id]

    def get_invitation_ids(self) -> List[str]:
        """获取邀请记录的ID列表"""
        if not self.team_data:
            return []

        ids = []
        invitations = self.extract_invitations_from_data(self.team_data)
        for invitation in invitations:
            ids.append(invitation.get('id', ''))

        return [id for id in ids if id]

    def extract_users_from_data(self, data) -> List[Dict]:
        """从数据中提取用户列表"""
        users = []
        if isinstance(data, dict):
            for key, value in data.items():
                # 支持多种字段名：users, members
                if key in ["users", "members"] and isinstance(value, list):
                    users.extend(value)
                elif isinstance(value, (dict, list)):
                    users.extend(self.extract_users_from_data(value))
        elif isinstance(data, list):
            for item in data:
                users.extend(self.extract_users_from_data(item))
        return users

    def extract_invitations_from_data(self, data) -> List[Dict]:
        """从数据中提取邀请列表"""
        invitations = []
        if isinstance(data, dict):
            for key, value in data.items():
                # 支持多种字段名：invitations, invites
                if key in ["invitations", "invites"] and isinstance(value, list):
                    invitations.extend(value)
                elif isinstance(value, (dict, list)):
                    invitations.extend(self.extract_invitations_from_data(value))
        elif isinstance(data, list):
            for item in data:
                invitations.extend(self.extract_invitations_from_data(item))
        return invitations

    def update_team_display(self):
        """更新团队数据显示"""
        if not self.team_data:
            return

        # 更新成员表格
        users = self.extract_users_from_data(self.team_data)
        self.update_members_table(users)

        # 更新邀请表格
        invitations = self.extract_invitations_from_data(self.team_data)
        self.update_invitations_table(invitations)

        # 更新统计卡片
        self.update_statistics(users, invitations)

        # 更新原始数据显示
        self.format_data_display()

    def update_statistics(self, users, invitations):
        """更新统计信息"""
        from datetime import datetime, date

        # 调试输出数据情况
        print(f"📋 统计数据源: 用户数量={len(users)}, 邀请数量={len(invitations)}")
        
        # 总成员数
        total_members = len(users)

        # 活跃成员数（已加入的成员）
        active_members = len([u for u in users if u.get('joinedAt')])

        # 待加入人数 = 邀请记录中的人数（未加入的人）
        pending_members = len(invitations)

        # 邀请记录中的总邀请 = 待加入人数
        total_invitations = pending_members
        
        # 更新统计卡片颜色
        self.update_stat_card_colors(active_members, pending_members, total_invitations)

        # 今日邀请人数（邀请时间为今天的邀请记录数）
        today = date.today()
        today_invited = 0
        for invitation in invitations:
            invited_at = invitation.get('invitedAt')
            if invited_at:
                try:
                    # 支持时间戳（int/float）或字符串
                    if isinstance(invited_at, (int, float)):
                        invite_date = datetime.fromtimestamp(invited_at / 1000).date()
                        print(f"处理时间戳: {invited_at} -> {invite_date}")
                    elif isinstance(invited_at, str) and len(invited_at) >= 10:
                        invite_date = datetime.fromisoformat(invited_at[:10]).date()
                        print(f"处理字符串时间: {invited_at} -> {invite_date}")
                    else:
                        continue
                    if invite_date == today:
                        today_invited += 1
                except Exception as e:
                    print(f"时间解析错误: {e}, 值类型: {type(invited_at)}, 值: {invited_at}")
                    continue

        # 记录统计结果
        print(f"📊 统计更新: 总成员={total_members}, 活跃={active_members}, 待加入={pending_members}, 邀请记录={total_invitations}, 今日邀请={today_invited}")
        
        try:
            # 直接更新统计卡片值
            if hasattr(self, 'total_members_card') and self.total_members_card is not None:
                self.total_members_card.value_label.setText(str(total_members))
                print(f"已更新总成员卡片: {total_members}")
                
            if hasattr(self, 'active_members_card') and self.active_members_card is not None:
                self.active_members_card.value_label.setText(str(active_members))
                print(f"已更新活跃成员卡片: {active_members}")
                
            if hasattr(self, 'pending_members_card') and self.pending_members_card is not None:
                self.pending_members_card.value_label.setText(str(pending_members))
                print(f"已更新待加入卡片: {pending_members}")
                
            if hasattr(self, 'total_invitations_card') and self.total_invitations_card is not None:
                self.total_invitations_card.value_label.setText(str(total_invitations))
                print(f"已更新总邀请卡片: {total_invitations}")
                
            if hasattr(self, 'recent_invitations_card') and self.recent_invitations_card is not None:
                self.recent_invitations_card.value_label.setText(str(today_invited))
                print(f"已更新今日邀请卡片: {today_invited}")
                
        except Exception as e:
            print(f"更新统计卡片时发生错误: {e}")
            self.log_error("统计更新", f"更新统计卡片时发生错误: {e}")
            
        # 记录统计更新成功
        self.log_info("统计更新", f"总成员: {total_members}个, 活跃: {active_members}个, 待加入: {pending_members}个, 今日邀请: {today_invited}个")

    def update_stat_card_value(self, card_type, value):
        """更新统计卡片的数值"""
        try:
            # 确保值为字符串
            value_str = str(value) if value is not None else "0"
            
            # 根据卡片类型更新对应的卡片值标签
            if card_type == "total_members" and hasattr(self, 'total_members_card'):
                self.total_members_card.value_label.setText(value_str)
            elif card_type == "active_members" and hasattr(self, 'active_members_card'):
                self.active_members_card.value_label.setText(value_str)
            elif card_type == "pending_members" and hasattr(self, 'pending_members_card'):
                self.pending_members_card.value_label.setText(value_str)
            elif card_type == "total_invitations" and hasattr(self, 'total_invitations_card'):
                self.total_invitations_card.value_label.setText(value_str)
            elif card_type == "recent_invitations" and hasattr(self, 'recent_invitations_card'):
                self.recent_invitations_card.value_label.setText(value_str)
            
            # 强制更新UI显示
            QApplication.processEvents()
        except Exception as e:
            print(f"更新统计卡片失败 ({card_type}): {e}")
            
    def update_stat_card_colors(self, active_members, pending_members, total_invitations):
        """更新统计卡片颜色，根据数值动态调整"""
        # 更新成员统计卡片颜色
        if hasattr(self, 'total_members_card'):
            self.total_members_card.setStyleSheet(f"""
                QFrame {{
                    background: white;
                    border-radius: 8px;
                    border-left: 4px solid {StyleManager.PRIMARY_COLOR};
                }}
            """)
            
        if hasattr(self, 'active_members_card'):
            self.active_members_card.setStyleSheet(f"""
                QFrame {{
                    background: white;
                    border-radius: 8px;
                    border-left: 4px solid {StyleManager.SUCCESS_COLOR};
                }}
            """)
            
        if hasattr(self, 'pending_members_card'):
            # 根据待加入人数调整颜色
            color = StyleManager.WARNING_COLOR
            if pending_members > 10:
                color = StyleManager.DANGER_COLOR
            elif pending_members == 0:
                color = StyleManager.SUCCESS_COLOR
                
            self.pending_members_card.setStyleSheet(f"""
                QFrame {{
                    background: white;
                    border-radius: 8px;
                    border-left: 4px solid {color};
                }}
            """)
            
        # 更新邀请统计卡片颜色
        if hasattr(self, 'total_invitations_card'):
            # 根据邀请总数调整颜色
            color = StyleManager.PRIMARY_COLOR
            if total_invitations > 10:
                color = StyleManager.WARNING_COLOR
            elif total_invitations > 20:
                color = StyleManager.DANGER_COLOR
                
            self.total_invitations_card.setStyleSheet(f"""
                QFrame {{
                    background: white;
                    border-radius: 8px;
                    border-left: 4px solid {color};
                }}
            """)
            
        if hasattr(self, 'recent_invitations_card'):
            self.recent_invitations_card.setStyleSheet(f"""
                QFrame {{
                    background: white;
                    border-radius: 8px;
                    border-left: 4px solid {StyleManager.WARNING_COLOR};
                }}
            """)
            
        # 更新邮箱验证卡片颜色 (如果存在)
        if hasattr(self, 'total_emails_card'):
            self.total_emails_card.setStyleSheet(f"""
                QFrame {{
                    background: white;
                    border-radius: 8px;
                    border-left: 4px solid {StyleManager.PRIMARY_COLOR};
                }}
            """)
            
        if hasattr(self, 'valid_emails_card'):
            self.valid_emails_card.setStyleSheet(f"""
                QFrame {{
                    background: white;
                    border-radius: 8px;
                    border-left: 4px solid {StyleManager.SUCCESS_COLOR};
                }}
            """)
            
        if hasattr(self, 'invalid_emails_card'):
            self.invalid_emails_card.setStyleSheet(f"""
                QFrame {{
                    background: white;
                    border-radius: 8px;
                    border-left: 4px solid {StyleManager.DANGER_COLOR};
                }}
            """)

    def update_members_table(self, users: List[Dict]):
        """更新成员表格 - 优化显示格式"""
        # 应用最大行数限制
        max_rows = self.config.get('ui.max_table_rows', 200)
        display_users = users[:max_rows] if len(users) > max_rows else users
        
        if len(users) > max_rows:
            self.log_warning("表格行数限制", f"成员表格已限制显示 {max_rows} 行，共 {len(users)} 条记录")
            
        self.members_table.setRowCount(len(display_users))

        for row, user in enumerate(display_users):
            # 序号
            seq_item = QTableWidgetItem(str(row + 1))
            seq_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.members_table.setItem(row, 0, seq_item)

            # ID - 截断显示但保留完整信息
            user_id = user.get('id', '')
            id_item = QTableWidgetItem(user_id)
            id_item.setToolTip(user_id)  # 鼠标悬停显示完整ID
            self.members_table.setItem(row, 1, id_item)

            # 邮箱
            email = user.get('email', '')
            email_item = QTableWidgetItem(email)
            email_item.setToolTip(email)  # 鼠标悬停显示完整邮箱
            self.members_table.setItem(row, 2, email_item)

            # 角色
            role = user.get('role', '未加入')
            role_item = QTableWidgetItem(role)
            role_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # 根据角色设置不同颜色
            if role == '未加入':
                role_item.setForeground(QColor('#dc3545'))  # 红色
            else:
                role_item.setForeground(QColor('#28a745'))  # 绿色
            self.members_table.setItem(row, 3, role_item)

            # 加入时间
            joined_at = user.get('joinedAt', '')
            if joined_at:
                try:
                    # 尝试格式化时间戳
                    if isinstance(joined_at, (int, float)):
                        joined_at = datetime.fromtimestamp(joined_at / 1000).strftime('%Y-%m-%d %H:%M')
                except:
                    pass
            time_item = QTableWidgetItem(str(joined_at) if joined_at else '未加入')
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.members_table.setItem(row, 4, time_item)

    def update_invitations_table(self, invitations: List[Dict]):
        """更新邀请表格 - 优化显示格式"""
        # 应用最大行数限制
        max_rows = self.config.get('ui.max_table_rows', 200)
        display_invitations = invitations[:max_rows] if len(invitations) > max_rows else invitations
        
        if len(invitations) > max_rows:
            self.log_warning("表格行数限制", f"邀请表格已限制显示 {max_rows} 行，共 {len(invitations)} 条记录")
            
        self.invitations_table.setRowCount(len(display_invitations))

        for row, invitation in enumerate(display_invitations):
            # 序号
            seq_item = QTableWidgetItem(str(row + 1))
            seq_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.invitations_table.setItem(row, 0, seq_item)

            # ID - 截断显示但保留完整信息
            inv_id = invitation.get('id', '')
            id_item = QTableWidgetItem(inv_id)
            id_item.setToolTip(inv_id)  # 鼠标悬停显示完整ID
            self.invitations_table.setItem(row, 1, id_item)

            # 邮箱
            email = invitation.get('email', '')
            email_item = QTableWidgetItem(email)
            email_item.setToolTip(email)  # 鼠标悬停显示完整邮箱
            email_item.setForeground(QColor('#fd7e14'))  # 橙色表示待处理
            self.invitations_table.setItem(row, 2, email_item)

            # 邀请时间
            invited_at = invitation.get('invitedAt', '')
            if invited_at:
                try:
                    # 尝试格式化时间戳
                    if isinstance(invited_at, (int, float)):
                        invited_at = datetime.fromtimestamp(invited_at / 1000).strftime('%Y-%m-%d %H:%M')
                except:
                    pass
            time_item = QTableWidgetItem(str(invited_at) if invited_at else '未知时间')
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.invitations_table.setItem(row, 3, time_item)

    def log_invite_history(self, message: str):
        """记录邀请历史"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        self.invite_history.append(log_entry)

    def log_batch_operation(self, message: str):
        """记录批量操作日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        self.batch_log.append(log_entry)

    def update_refresh_timer(self):
        """更新自动刷新定时器"""
        if self.config.get('ui.auto_refresh', True):
            interval = self.config.get('ui.refresh_interval', 30) * 1000  # 转换为毫秒
            self.refresh_timer.start(interval)
            self.log_info("自动刷新", f"已启用自动刷新，间隔: {interval/1000} 秒")
        else:
            self.refresh_timer.stop()
            self.log_info("自动刷新", "已禁用自动刷新")

    def auto_refresh_data(self):
        """自动刷新数据"""
        if self.team_data and not (self.worker_thread and self.worker_thread.isRunning()):
            self.load_team_data()

    # ==================== 菜单事件处理 ====================

    def open_config_dialog(self):
        """打开配置对话框"""
        dialog = ConfigDialog(self.config, self)
        # 连接配置更改信号
        dialog.config_changed.connect(self.apply_config)
        dialog.show()

    def apply_config(self):
        """应用新的配置设置"""
        print("正在应用新的配置设置...")
        # 重新初始化API客户端
        self.api_client = APIClient(self.config)
        
        # 更新刷新定时器
        self.update_refresh_timer()
        
        # 应用UI样式和主题
        app = QApplication.instance()
        app.setStyleSheet(StyleManager.get_app_style())
        
        # 更新字体大小
        font_size = self.config.get('ui.font_size', 10)
        font = app.font()
        font.setPointSize(font_size)
        app.setFont(font)
        
        # 应用透明度
        opacity = self.config.get('ui.opacity', 100) / 100
        self.setWindowOpacity(opacity)
        
        # 应用动画和阴影设置
        self.apply_visual_effects()
        
        # 更新表格行数限制
        self.apply_table_row_limit()
        
        # 更新其他UI元素
        self.log_success("配置更新", "配置已更新并应用")
        
        # 如果有数据，刷新显示
        if self.team_data:
            self.update_team_display()
            
    def apply_visual_effects(self):
        """应用视觉效果"""
        # 获取动画和阴影设置
        animations_enabled = self.config.get('ui.animations', True)
        shadows_enabled = self.config.get('ui.shadows', True)
        
        # 应用到主要UI元素
        if hasattr(self, 'tab_widget'):
            if shadows_enabled:
                StyleManager.apply_shadow_effect(self.tab_widget, blur_radius=15, offset=(0, 5))
            else:
                self.tab_widget.setGraphicsEffect(None)
        
        # 处理所有组信息卡片
        self.apply_effect_to_cards(shadows_enabled)
        
        # 记录设置状态
        self.log_info("视觉效果", 
                     f"{'已启用' if animations_enabled else '已禁用'}动画效果, "
                     f"{'已启用' if shadows_enabled else '已禁用'}阴影效果")
    
    def apply_effect_to_cards(self, shadows_enabled):
        """应用效果到所有卡片"""
        # 查找所有可能的卡片和组件，应用阴影效果
        for widget in self.findChildren(QGroupBox):
            if shadows_enabled:
                StyleManager.apply_shadow_effect(widget, blur_radius=8, offset=(0, 3))
            else:
                widget.setGraphicsEffect(None)
                
        # 应用到统计卡片
        stat_cards = [
            'total_members_card', 'active_members_card', 'pending_members_card',
            'total_invitations_card', 'recent_invitations_card',
            'total_emails_card', 'valid_emails_card', 'invalid_emails_card'
        ]
        
        for card_name in stat_cards:
            if hasattr(self, card_name):
                card = getattr(self, card_name)
                if shadows_enabled:
                    StyleManager.apply_shadow_effect(card, blur_radius=10, offset=(0, 3))
                else:
                    card.setGraphicsEffect(None)
    
    def apply_table_row_limit(self):
        """应用表格行数限制"""
        max_rows = self.config.get('ui.max_table_rows', 200)
        
        # 记录设置
        self.log_info("表格设置", f"表格最大行数限制为 {max_rows} 行")
        
        # 重新显示数据会自动应用这个限制
        if self.team_data:
            self.update_team_display()

    def import_config(self):
        """导入配置"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入配置文件", "", "JSON文件 (*.json);;所有文件 (*)"
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    imported_config = json.load(f)

                # 合并配置
                self.config.config = self.config._merge_config(self.config.default_config, imported_config)
                self.config.save_config()

                # 应用新配置
                self.apply_config()

                self.log_success("配置导入", "配置导入成功并已应用！")
            except Exception as e:
                self.log_error("配置导入失败", f"导入配置失败: {str(e)}")

    def export_config(self):
        """导出配置"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出配置文件",
            f"team_manager_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON文件 (*.json);;所有文件 (*)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.config.config, f, indent=2, ensure_ascii=False)
                self.log_success("配置导出", f"配置已导出到: {file_path}")
            except Exception as e:
                self.log_error("配置导出失败", f"导出配置失败: {str(e)}")

    def show_about(self):
        """显示关于信息"""
        about_info = (
            "团队管理工具 v1.0 - 功能强大的团队成员管理工具，"
            "支持批量邀请成员、查看团队信息、批量删除操作、数据导出功能、灵活的配置管理。"
            "技术栈: Python 3.8+, PyQt6, Requests"
        )
        self.log_info("关于应用", about_info)

    # 增加获取连接状态的方法
    def get_connection_status(self):
        """获取当前连接状态"""
        return self.is_connected


def main():
    """主程序入口"""
    app = QApplication(sys.argv)

    # 设置应用信息
    app.setApplicationName("🛠️ 团队管理工具")
    app.setApplicationDisplayName("团队管理工具")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Team Manager")
    app.setOrganizationDomain("teammanager.local")

    # 设置应用样式
    app.setStyle('Fusion')

    # 设置应用字体
    try:
        font = QFont("Microsoft YaHei UI", 9)
        app.setFont(font)
    except:
        # 如果字体设置失败，使用默认字体
        pass

    # 设置应用图标（如果有的话）
    # app.setWindowIcon(QIcon("team_manager_icon.png"))

    try:
        # 创建主窗口
        window = TeamManagerMainWindow()

        # 居中显示窗口
        try:
            screen = app.primaryScreen().geometry()
            window_size = window.geometry()
            x = (screen.width() - window_size.width()) // 2
            y = (screen.height() - window_size.height()) // 2
            window.move(x, y)
        except:
            # 如果居中失败，使用默认位置
            pass

        window.show()

        # 显示启动消息
        try:
            window.status_label.setText("应用启动成功，请配置API设置后开始使用")
        except:
            pass

        print("🎉 团队管理工具启动成功！")
        print("💡 提示：请在 工具 -> 配置设置 中配置API信息")

        # 运行应用
        sys.exit(app.exec())

    except Exception as e:
        # 错误处理
        print(f"❌ 应用启动失败: {str(e)}")
        try:
            # 创建一个临时的父窗口用于显示错误消息
            temp_widget = QWidget()
            CustomMessageBox.show_error(temp_widget, "启动错误",
                                      f"应用启动失败：{str(e)}\n\n"
                                      f"错误详情：\n{str(e)}")
            # 等待一段时间让用户看到错误消息
            QTimer.singleShot(5000, app.quit)
            app.exec()
        except:
            # 如果连错误对话框都无法显示，直接打印错误
            print(f"详细错误信息：{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
