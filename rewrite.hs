import Text.JSON
import Text.Printf
import Data.String.Utils
import System.Environment
import qualified Data.Map as M
import System.IO

myDecode s = case decode s of
               Ok a -> return a
               Error s -> fail s

main = do
  hSetBuffering stdout NoBuffering
  [scandir, csvpaths] <- getArgs
  printf "About to read albums\n"
  albums <- (readFile (scandir ++ "/albums.info") >>= myDecode)::IO (M.Map String (M.Map String String))
  printf "Read albums\n"
  csvdata <- readFile csvpaths
  let csv = foldl (\m [k, v] -> M.insert k v m) M.empty . map (split ",")
            . lines $ csvdata
  mapM_ (procAlbum scandir csv) (M.toList albums)
  
(!) = (M.!)

procAlbum :: String -> M.Map String String -> (String, M.Map String String) -> IO ()
procAlbum scandir csv (album, albuminfo) =
    do printf "\n\n######## Album %s: %s\n" album (albuminfo ! "title")
       if M.member "flickrurl" albuminfo
          then if M.member album csv
                    then printf "RewriteRule ^/v/%s($|/$) %s [R=permanent,L]\n" 
                         (csv ! album) (albuminfo ! "flickrurl")
                    else printf "## FIXME: No CSV for album %s: %s\n" 
                         album (albuminfo ! "title") 
          else printf "## FIXME: No Flickr URL for album!\n"
              
       images <- readFile (printf "%s/%s/images.info" scandir album) 
                 >>= myDecode
       mapM_ (procImage album csv) images

procImage album csv image =
    if M.member (image ! "name") csv
    then do printf "RewriteRule ^/v/%s/%s.html$ %s [R=permanent,L]\n"
              (csv ! album) (csv ! (image ! "name")) (image ! "flickrpage")
            printf "RewriteRule ^/main.php?g2_view=core%%3AShowItem&g2_itemId=%s(&|$) %s [R=permanent,L]\n"
              (image ! "name") (image ! "flickrpage")
            printf "RewriteRule ^/d/%s-([0-9]+)/%s$ %s [R=permanent,L]\n"
              (image ! "name") (csv ! (image ! "name")) (image ! "flickrimg")
            printf "RewriteRule ^/main.php?g2_view=core%%3ADownloadItem&g2_itemId=%s(&|$) %s [R=permanent,L]\n\n"
              (image ! "name") (image ! "flickrimg")
    else printf "# FIXME: no entry in CSV for image %s\n" (image ! "name")
