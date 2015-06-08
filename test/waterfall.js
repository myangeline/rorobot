/**
 * Created by sunshine on 2015/6/8.
 */
(function (F, D, E) {
    var B = D.event, C;
    B.special.smartresize = {
        setup: function () {
            D(this).bind("resize", B.special.smartresize.handler)
        }, teardown: function () {
            D(this).unbind("resize", B.special.smartresize.handler)
        }, handler: function (K, I) {
            var J = this, H = arguments;
            K.type = "smartresize", C && clearTimeout(C), C = setTimeout(function () {
                jQuery.event.handle.apply(J, H)
            }, I === "execAsap" ? 0 : 100)
        }
    }, D.fn.smartresize = function (H) {
        return H ? this.bind("smartresize", H) : this.trigger("smartresize", ["execAsap"])
    }, D.Mason = function (I, H) {
        this.element = D(H), this._create(I), this._init()
    };
    var G = ["position", "height"];
    D.Mason.settings = {
        isResizable: !0,
        isAnimated: !1,
        animationOptions: {queue: !1, duration: 500},
        gutterWidth: 0,
        isRTL: !1,
        isFitWidth: !1
    }, D.Mason.prototype = {
        _filterFindBricks: function (I) {
            var H = this.options.itemSelector;
            return H ? I.filter(H).add(I.find(H)) : I
        }, _getBricks: function (I) {
            var H = this._filterFindBricks(I).css({position: "absolute"}).addClass("masonry-brick");
            return H
        }, _create: function (M) {
            this.options = D.extend(!0, {}, D.Mason.settings, M), this.styleQueue = [], this.reloadItems();
            var I = this.element[0].style;
            this.originalStyle = {};
            for (var J = 0, H = G.length; J < H; J++) {
                var K = G[J];
                this.originalStyle[K] = I[K] || null
            }
            this.element.css({position: "relative"}), this.horizontalDirection = this.options.isRTL ? "right" : "left", this.offset = {};
            var L = D(document.createElement("div"));
            this.element.prepend(L), this.offset.y = Math.round(L.position().top), this.options.isRTL ? (L.css({
                "float": "right",
                display: "inline-block"
            }), this.offset.x = Math.round(this.element.outerWidth() - L.position().left)) : this.offset.x = Math.round(L.position().left), L.remove();
            var N = this;
            setTimeout(function () {
                N.element.addClass("masonry")
            }, 0), this.options.isResizable && D(F).bind("smartresize.masonry", function () {
                N.resize()
            })
        }, _init: function (H) {
            this._getColumns("masonry"), this._reLayout(H)
        }, option: function (I, H) {
            D.isPlainObject(I) && (this.options = D.extend(!0, this.options, I))
        }, layout: function (R, Q) {
            var U, H, S, T, K, L;
            for (var I = 0, J = R.length; I < J; I++) {
                U = D(R[I]), H = Math.ceil(U.outerWidth(!0) / this.columnWidth), H = Math.min(H, this.cols);
                if (H === 1) {
                    this._placeBrick(U, this.colYs)
                } else {
                    S = this.cols + 1 - H, T = [];
                    for (L = 0; L < S; L++) {
                        K = this.colYs.slice(L, L + H), T[L] = Math.max.apply(Math, K)
                    }
                    this._placeBrick(U, T)
                }
            }
            var O = {};
            O.height = Math.max.apply(Math, this.colYs) - this.offset.y, this.options.isFitWidth && (O.width = this.cols * this.columnWidth - this.options.gutterWidth), this.styleQueue.push({
                $el: this.element,
                style: O
            });
            var P = this.isLaidOut ? this.options.isAnimated ? "animate" : "css" : "css", M = this.options.animationOptions, N;
            for (I = 0, J = this.styleQueue.length; I < J; I++) {
                N = this.styleQueue[I], N.$el[P](N.style, M)
            }
            this.styleQueue = [], Q && Q.call(R), this.isLaidOut = !0
        }, _getColumns: function () {
            var I = this.options.isFitWidth ? this.element.parent() : this.element, H = I.width();
            this.columnWidth = this.options.columnWidth || this.$bricks.outerWidth(!0) || H, this.columnWidth += this.options.gutterWidth, this.cols = Math.floor((H + this.options.gutterWidth) / this.columnWidth), this.cols = Math.max(this.cols, 1)
        }, _placeBrick: function (M, K) {
            var L = Math.min.apply(Math, K), P = 0;
            for (var H = 0, N = K.length; H < N; H++) {
                if (K[H] === L) {
                    P = H;
                    break
                }
            }
            var O = {top: L};
            O[this.horizontalDirection] = this.columnWidth * P + this.offset.x, this.styleQueue.push({
                $el: M,
                style: O
            });
            var I = L + M.outerHeight(!0), J = this.cols + 1 - N;
            for (H = 0; H < J; H++) {
                this.colYs[P + H] = I
            }
        }, resize: function () {
            var H = this.cols;
            this._getColumns("masonry"), this.cols !== H && this._reLayout()
        }, _reLayout: function (I) {
            var H = this.cols;
            this.colYs = [];
            while (H--) {
                this.colYs.push(this.offset.y)
            }
            this.layout(this.$bricks, I)
        }, reloadItems: function () {
            this.$bricks = this._getBricks(this.element.children())
        }, reload: function (H) {
            this.reloadItems(), this._init(H)
        }, appended: function (K, I, J) {
            if (I) {
                this._filterFindBricks(K).css({top: this.element.height()});
                var H = this;
                setTimeout(function () {
                    H._appended(K, J)
                }, 1)
            } else {
                this._appended(K, J)
            }
        }, _appended: function (J, H) {
            var I = this._getBricks(J);
            this.$bricks = this.$bricks.add(I), this.layout(I, H)
        }, remove: function (H) {
            this.$bricks = this.$bricks.not(H), H.remove()
        }, destroy: function () {
            this.$bricks.removeClass("masonry-brick").each(function () {
                this.style.position = null, this.style.top = null, this.style.left = null
            });
            var K = this.element[0].style;
            for (var I = 0, J = G.length; I < J; I++) {
                var H = G[I];
                K[H] = this.originalStyle[H]
            }
            this.element.unbind(".masonry").removeClass("masonry").removeData("masonry"), D(F).unbind(".masonry")
        }
    }, D.fn.imagesLoaded = function (L) {
        var K = this.find("img"), I = K.length, J = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==", M = this, H = function () {
            --I <= 0 && this.src !== J && (L.call(M), K.unbind("load", H))
        };
        if (!I) {
            L.call(this);
            return this
        }
        K.bind("load", H).each(function () {
            if (this.complete || this.complete === E) {
                var N = this.src;
                this.src = J, this.src = N
            }
        });
        return this
    };
    var A = function (H) {
        this.console && console.error(H)
    };
    D.fn.masonry = function (I) {
        if (typeof I == "string") {
            var H = Array.prototype.slice.call(arguments, 1);
            this.each(function () {
                var J = D.data(this, "masonry");
                if (!J) {
                    A("cannot call methods on masonry prior to initialization; attempted to call method '" + I + "'")
                } else {
                    if (!D.isFunction(J[I]) || I.charAt(0) === "_") {
                        A("no such method '" + I + "' for masonry instance");
                        return
                    }
                    J[I].apply(J, H)
                }
            })
        } else {
            this.each(function () {
                var J = D.data(this, "masonry");
                J ? (J.option(I || {}), J._init()) : D.data(this, "masonry", new D.Mason(I, this))
            })
        }
        return this
    }
})(window, jQuery);
$(document).ready(function () {
    if ($("#container").length > 0) {
        $("#container").masonry({itemSelector: ".col", singleMode: true});
        $(".mby").css({"visibility": "visible"}).slideDown();
        $(".iloading").hide()
    }
});
$(window).scroll(function () {
    if ($(document).height() - $(this).scrollTop() - $(this).height() < 100) {
        showMoreCaiPu()
    }
});
function showMoreCaiPu() {
    var C = $("#param");
    var A = parseInt(C.attr("offset"));
    var B = C.attr("cate");
    if (A < 12) {
        $("#param").ajaxStart(function () {
            $(window).unbind("scroll", showMoreCaiPu)
        });
        A = A + 12;
        C.attr("offset", A);
        $("#showloading").show();
        $.ajax({
            type: "post",
            url: "/uajax/getMoreCaipu",
            data: "offset=" + A + "&cate=" + B,
            dataType: "text",
            async: false,
            success: function (E) {
                var D = $(E);
                $(window).scroll(showMoreCaiPu);
                D.hide();
                $("#container").append(D).masonry("appended", D);
                D.fadeIn(1000);
                $(".pagediv").show()
            }
        });
        $("#showloading").hide()
    } else {
        $(window).unbind("scroll", showMoreCaiPu)
    }
};
$(window).ready(function () {
    $(".course").live({
        mouseover: function () {
            var A = $(this).attr("data-id");
            $("." + A).removeClass("hidden")
        }, mouseout: function () {
            var A = $(this).attr("data-id");
            $("." + A).addClass("hidden")
        }
    })
});
$(".shoucanginfo").live("click", function () {
    var B = $(this).attr("shoucangstatus");
    var A = $(this).attr("cook_id");
    if (A) {
        $.ajax({
            type: "post",
            url: "/uajax/addDelCollectInfo",
            data: "&cookid=" + A + "&status=" + B,
            dataType: "json",
            success: function (D) {
                if (D.data == "NoLogin") {
                    logindialog()
                } else {
                    if (D.data == "slice") {
                        showerrorinfo("鎻愮ず", "鎮ㄤ粛澶勫湪绂佽█鏈熷唴锛屼笉鑳藉彂琛ㄥ唴瀹广€�")
                    } else {
                        if (D.data == "HAS") {
                            alert("姝よ彍璋卞凡鏀惰棌锛�")
                        } else {
                            if (D.data == "EMPTYINFO") {
                                alert("鑿滆氨涓嶅瓨鍦紒")
                            } else {
                                if (D.data == "ERROR") {
                                    alert("鏀惰棌澶辫触锛�")
                                } else {
                                    var C = B == 0 ? 1 : 0;
                                    $("#shoucangstatus" + A).attr("shoucangstatus", C);
                                    B == 0 ? $("#shoucangstatus" + A).removeClass("bu_sc").addClass("bu_qxsc") : $("#shoucangstatus" + A).removeClass("bu_qxsc").addClass("bu_sc")
                                }
                            }
                        }
                    }
                }
            }
        })
    }
});