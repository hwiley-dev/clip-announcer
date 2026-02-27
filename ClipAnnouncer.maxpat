{
  "patcher": {
    "fileversion": 1,
    "appversion": {
      "major": 9,
      "minor": 0,
      "revision": 10,
      "architecture": "x64",
      "modernui": 1
    },
    "classnamespace": "box",
    "rect": [
      60.0,
      120.0,
      820.0,
      460.0
    ],
    "openinpresentation": 1,
    "gridsize": [
      15.0,
      15.0
    ],
    "boxes": [
      {
        "box": {
          "hidden": 1,
          "id": "obj-1",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            24.0,
            18.0,
            220.0,
            20.0
          ],
          "text": "Clip Announcer (3-Button Beta)"
        }
      },
      {
        "box": {
          "id": "obj-2",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            18.0,
            90.0,
            56.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            18.0,
            74.0,
            56.0,
            20.0
          ],
          "text": "WHERE"
        }
      },
      {
        "box": {
          "id": "obj-3",
          "maxclass": "live.button",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "parameter_enable": 1,
          "patching_rect": [
            110.0,
            50.0,
            36.0,
            36.0
          ],
          "presentation": 1,
          "presentation_rect": [
            18.0,
            16.0,
            56.0,
            56.0
          ],
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_enum": [
                "off",
                "on"
              ],
              "parameter_longname": "where_button",
              "parameter_mmax": 1,
              "parameter_modmode": 0,
              "parameter_shortname": "where_button",
              "parameter_type": 2
            }
          },
          "varname": "where_button"
        }
      },
      {
        "box": {
          "id": "obj-16",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            92.0,
            90.0,
            56.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            92.0,
            74.0,
            56.0,
            20.0
          ],
          "text": "WHAT"
        }
      },
      {
        "box": {
          "id": "obj-17",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            166.0,
            90.0,
            56.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            166.0,
            74.0,
            56.0,
            20.0
          ],
          "text": "STATE"
        }
      },
      {
        "box": {
          "id": "obj-18",
          "maxclass": "live.button",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "parameter_enable": 1,
          "patching_rect": [
            184.0,
            50.0,
            36.0,
            36.0
          ],
          "presentation": 1,
          "presentation_rect": [
            92.0,
            16.0,
            56.0,
            56.0
          ],
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_enum": [
                "off",
                "on"
              ],
              "parameter_longname": "what_button",
              "parameter_mmax": 1,
              "parameter_modmode": 0,
              "parameter_shortname": "what_button",
              "parameter_type": 2
            }
          },
          "varname": "what_button"
        }
      },
      {
        "box": {
          "id": "obj-19",
          "maxclass": "live.button",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "parameter_enable": 1,
          "patching_rect": [
            258.0,
            50.0,
            36.0,
            36.0
          ],
          "presentation": 1,
          "presentation_rect": [
            166.0,
            16.0,
            56.0,
            56.0
          ],
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_enum": [
                "off",
                "on"
              ],
              "parameter_longname": "state_button",
              "parameter_mmax": 1,
              "parameter_modmode": 0,
              "parameter_shortname": "state_button",
              "parameter_type": 2
            }
          },
          "varname": "state_button"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-20",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            110.0,
            90.0,
            98.0,
            22.0
          ],
          "text": "announce_where"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-21",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            220.0,
            90.0,
            92.0,
            22.0
          ],
          "text": "announce_what"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-22",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            324.0,
            90.0,
            95.0,
            22.0
          ],
          "text": "announce_state"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-6",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            190.0,
            56.0,
            140.0,
            22.0
          ],
          "saved_object_attributes": {
            "filename": "clip_announcer.js",
            "parameter_enable": 0
          },
          "text": "js clip_announcer.js"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-7",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            344.0,
            56.0,
            260.0,
            22.0
          ],
          "saved_object_attributes": {
            "autostart": 1,
            "defer": 0,
            "node_bin_path": "",
            "npm_bin_path": "",
            "watch": 0
          },
          "text": "node.script clip_announcer_tts.js @autostart 1",
          "textfile": {
            "filename": "clip_announcer_tts.js",
            "flags": 0,
            "embed": 0,
            "autowatch": 1
          }
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-8",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 3,
          "outlettype": [
            "bang",
            "int",
            "int"
          ],
          "patching_rect": [
            24.0,
            110.0,
            90.0,
            22.0
          ],
          "text": "live.thisdevice"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-9",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            126.0,
            110.0,
            33.0,
            22.0
          ],
          "text": "init"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-10",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            171.0,
            110.0,
            79.0,
            22.0
          ],
          "text": "dump_state"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-12",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            262.0,
            110.0,
            72.0,
            22.0
          ],
          "text": "speak_test"
        }
      },
      {
        "box": {
          "hidden": 1,
          "id": "obj-11",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            24.0,
            160.0,
            620.0,
            20.0
          ],
          "text": "Selection state + summary logs are printed to the Max Console by clip_announcer.js"
        }
      }
    ],
    "lines": [
      {
        "patchline": {
          "destination": [
            "obj-6",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-10",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-7",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-12",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-20",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-3",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-7",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-6",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-6",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-20",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-21",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-18",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-6",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-21",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-22",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-19",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-6",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-22",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-9",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-8",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-6",
            0
          ],
          "hidden": 1,
          "source": [
            "obj-9",
            0
          ]
        }
      }
    ],
    "parameters": {
      "obj-3": [
        "where_button",
        "where_button",
        0
      ],
      "obj-18": [
        "what_button",
        "what_button",
        0
      ],
      "obj-19": [
        "state_button",
        "state_button",
        0
      ],
      "inherited_shortname": 1
    },
    "dependency_cache": [
      {
        "name": "clip_announcer.js",
        "bootpath": "~/Code Projects/Clip Announcer",
        "patcherrelativepath": ".",
        "type": "TEXT",
        "implicit": 1
      },
      {
        "name": "clip_announcer_tts.js",
        "bootpath": "~/Code Projects/Clip Announcer",
        "patcherrelativepath": ".",
        "type": "TEXT",
        "implicit": 1
      }
    ],
    "autosave": 0,
    "oscreceiveudpport": 0
  }
}
